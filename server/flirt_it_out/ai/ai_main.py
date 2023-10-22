import multiprocessing
import random

from ctransformers import AutoModelForCausalLM

class User:
    def __init__(self, name: str, ai_name="you", user_id = 0):
        self.name = name
        self.ai_name = ai_name
        self.user_id = user_id
        self.messages = []

    def add_message(self, message: str):
        self.messages.append(message)

    def remove_message(self, index = None):
        if index is None:
            self.messages.pop()
        else:
            self.messages.pop(index)

    def change_message(self, index, message):
        if len(self.messages) <= index:
            raise ValueError(f"Index '{index}' is out of range.")

        self.messages[index] = message

    def combined_messages(self):
        if not self.messages:
            return ""

        combined = "<|im_start|>system\n" + self.messages[0] + "<|im_end|>\n"
        for idx, msg in enumerate(self.messages[1:], start=1):
            if idx % 2 == 1:  # AI's turn
                combined += "<|im_start|>" + self.ai_name + "\n"
            else:  # User's turn
                combined += "<|im_start|>" + self.name + "\n"
            combined += msg + "<|im_end|>\n"
        return combined

    def __repr__(self):
        return f"User(name={self.name}, ai_name={self.ai_name}, messages={self.messages})"


class Model:
    def __init__(self, cd ="./mistral-7b-openorca.Q4_K_M.gguf"):
        self.model = self._load_model(cd)

        self.ai_name = None
        self.ai_description = None
        self.ai_first_message = None
        self.users = {}  # Dictionary to store users by their user_id

    def _load_model(self, model_path):
        return AutoModelForCausalLM.from_pretrained(
            model_path,
            #model_file=model_file,
            #model_type="mistral",
            gpu_layers=50,
            stop=["<|im_end|>", "<|i"],
            max_new_tokens=64,
            context_length=4096,
            local_files_only=True,
            threads=multiprocessing.cpu_count() - 2,
            stream=False,
        )

    def add_user(self, user_name: str, user_id: int):
        """Adds a new user with the given name and returns their user_id."""
        if user_id in self.users:
            raise ValueError(f"User with user_id '{user_id}' already exists.")
        self.users[user_id] = User(user_name, ai_name=self.ai_name, user_id=user_id)

    def remove_user(self, user_id: int):
        """Removes a user with the given user_id."""
        if user_id not in self.users:
            raise ValueError(f"User with user_id '{user_id}' does not exist.")
        del self.users[user_id]

    def start_game(self, ai_name=None, ai_description=None, ai_first_message=None):
        if ai_name is not None:
            self.ai_name = ai_name

        if ai_description is not None:
            self.ai_description = ai_description + " Keep all responses under 3 sentences."

        if ai_first_message is not None:
            self.ai_first_message = ai_first_message

        # Update ai_name for all users
        for user in self.users.values():
            user.ai_name = self.ai_name
            user.add_message(self.ai_description)
            user.add_message(self.ai_first_message)

        #self.model(self.users[min(self.users.keys())].combined_messages(), max_new_tokens=0)

    def rate_all_chats(self):
        """Rates the chats of all users"""
        for user in self.users.values():
            num, text = self.rate_chat(user.user_id)
            yield user.user_id, num, text

    def rate_chat(self, user_id):
        user = self.users[user_id]
        user.change_message(0, f"Rate this message stream based on how well {user.name} did trying to impress {user.ai_name}. Be very strict in your ratings. Give a score out of 10. Give a very brief one sentence explanation after giving your rating.")

        input_string = user.combined_messages() + f"<|im_start|>CONVERSATION RATER\nI would give {user.name} a score out of 10 of: ("

        output = self.model(input_string).split(')', 1)

        try:
            num = float(output[0].strip(')').split('/')[0])
            text = output[1].strip('\n').strip('.').strip()
        except:
            num = random.randrange(0, 10)
            text = ''

        if len(text) <= 2:
            text = user.name + self.model(input_string + str(num) + f')\n{user.name}')

        return num, text.rstrip()

    def message_history(self, user_id):
        return self.users[user_id].messages[1:]

    def change_message(self, user_id, index, message):
        """Changes message of a user"""
        if user_id not in self.users:
            raise ValueError(f"User with user_id '{user_id}' does not exist.")

        self.users[user_id].change_message(index, message)

    def send_message(self, user_id: int, message: str, generate=True):
        """Sends a new message to a user given their user_id."""
        if user_id not in self.users:
            raise ValueError(f"User with user_id '{user_id}' does not exist.")

        user = self.users[user_id]
        self.users[user_id].add_message(message)

        if not generate:
            return

        response = self.model(user.combined_messages() + "<|im_start|>" + self.ai_name + "\n").rstrip()

        user.add_message(response)
        return response

    def __repr__(self):
        return f"Model(ai_name={self.ai_name}, ai_description={self.ai_description}, users={self.users})"


def run():
    # Create an instance of the Model class
    model = Model()

    # Add a user
    users = ["John", "Will", "Henry"]

    id = 0
    for user in users:
        model.add_user(user_name=user, user_id=id)
        id += 1

    model.start_game(ai_name="Joe Biden", ai_description="You are Joe Biden, often characterized as empathetic and personable, with a long history in public service that has seen you face both personal and political challenges. You are known for your approachability and your tendency to speak candidly, sometimes leading to gaffes. Biden values personal relationships and has a reputation for reaching across the aisle in your efforts to achieve legislative compromise.", ai_first_message="Hey cutie *winks*. Wanna see something... *pulls on shirt*.")

    for user_id in range(len(users)):
        print(model.send_message(user_id, "Hello Mr. President."))
        print(model.send_message(user_id, "I want to kiss you on your beautiful lips *licks lips*"))

    for rating in model.rate_all_chats():
        print(rating)