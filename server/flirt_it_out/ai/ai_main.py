import multiprocessing
from ctransformers import AutoModelForCausalLM

class User:
    def __init__(self, name: str, ai_name="you", user_id = 0):
        self.name = name
        self.ai_name = ai_name
        self.messages = []

    def add_message(self, message: str):
        self.messages.append(message)

    def remove_message(self, index = None):
        if index is None:
            self.messages.pop()
        else:
            self.messages.pop(index)

    def combined_messages(self):
        if not self.messages:
            return ""

        combined = "<start>system\n" + self.messages[0] + "<end>\n"
        for idx, msg in enumerate(self.messages[1:], start=1):
            if idx % 2 == 1:  # AI's turn
                combined += "<start>" + self.ai_name + "\n"
            else:  # User's turn
                combined += "<start>" + self.name + "\n"
            combined += msg + "<end>\n"
        return combined

    def __repr__(self):
        return f"User(name={self.name}, ai_name={self.ai_name}, messages={self.messages})"


class Model:
    def __init__(self, ai_name: str, ai_description: str, ai_first_message: str):
        self.model = self._load_model()

        self.ai_name = ai_name
        self.ai_description = ai_description
        self.ai_first_message = ai_first_message
        self.users = {}  # Dictionary to store users by their user_id

    def _load_model(self):
        return AutoModelForCausalLM.from_pretrained(
            "/home/ethan/flirt-it-out/server/flirt_it_out/ai/ai_models/mistral-7b-openorca.Q4_K_M.gguf",
            #model_file=model_file,
            model_type="mistral",
            gpu_layers=50,
            stop=["<|im_end|>"],
            max_new_tokens=96,
            context_length=4096,
            local_files_only=True,
            threads=multiprocessing.cpu_count() - 2,
        )

    def add_user(self, user_name: str, user_id: int) -> int:
        """Adds a new user with the given name and returns their user_id."""
        if user_id in self.users:
            raise ValueError(f"User with user_id '{user_id}' already exists.")
        self.users[user_id] = User(user_name, self.ai_name, user_id)

    def remove_user(self, user_id: int):
        """Removes a user with the given user_id."""
        if user_id not in self.users:
            raise ValueError(f"User with user_id '{user_id}' does not exist.")
        del self.users[user_id]

    def update_ai_info(self, ai_name: str, ai_description: str, ai_first_message: str):
        """Updates AI name, description, and first message."""
        self.ai_name = ai_name
        self.ai_description = ai_description
        self.ai_first_message = ai_first_message

        # Update ai_name for all users
        for user in self.users.values():
            user.ai_name = ai_name

            user.remove_message()
            user.remove_message()

            user.add_message(ai_description)
            user.add_message(ai_first_message)


    def send_message(self, user_id: int, message: str, generate: bool):
        """Sends a new message to a user given their user_id."""
        if user_id not in self.users:
            raise ValueError(f"User with user_id '{user_id}' does not exist.")
        self.users[user_id].add_message(message)

    def add_message_to_all(self, message: str, generate: bool):
        """Sends a message to all users."""
        for user in self.users.values():
            user.add_message(message)

    def remove_message_from_all(self, index = None):
        """Removes a message from all users."""
        for user in self.users.values():
            user.remove_message(index)

    def __repr__(self):
        return f"Model(ai_name={self.ai_name}, ai_description={self.ai_description}, users={self.users})"


def run():
    def load_model():
        return AutoModelForCausalLM.from_pretrained(
            "/home/ethan/flirt-it-out/server/flirt_it_out/ai/ai_models/mistral-7b-openorca.Q4_K_M.gguf",
            #model_file=model_file,
            model_type="mistral",
            gpu_layers=50,
            stop=["<|im_end|>"],
            max_new_tokens=96,
            context_length=4096,
            local_files_only=True,
            threads=multiprocessing.cpu_count() - 2,
        )

    model = load_model()

    user_names = ["user0", "user1"]
    ai_name = "Emily"
    ai_description = f"You are {ai_name}, a woman who is looking for a romantic partner. You want to make sure that the partner you pick is the right one. Keep responses under three sentences. If they ask off topic questions or don't make sense, call them out on it."
    ai_first_message = "Hey glad you could make it, I love the food here."

    message_dict = dict(zip(user_names, [
        '\n'.join((
            f"<|im_start|>system",
            f"{user}{ai_description}<|im_end|>",
            f"<|im_start|>{ai_name}",
            f"{ai_first_message}<|im_end|>",
            f"<|im_start|>{user}",
            f"I've always wondered what it would be like to be in the same room as a hippo *looks at you with an evil grin*.<|im_end|>",
            f"<|im_start|>{ai_name}\n"
        ))
        for user in user_names
    ]))

    for user in user_names:
        generate = model(message_dict[user], stream=True)

        print(message_dict[user], end="", flush=True)
        for text in generate:
            print(text, end="", flush=True)