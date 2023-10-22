import multiprocessing
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
    def __init__(self, ai_name: str, ai_description: str, ai_first_message: str, model_path="/home/ethan/flirt-it-out/server/flirt_it_out/ai/ai_models/mistral-7b-openorca.Q4_K_M.gguf"):
        self.model = self._load_model(model_path)

        self.ai_name = ai_name
        self.ai_description = ai_description
        self.ai_first_message = ai_first_message
        self.users = {}  # Dictionary to store users by their user_id

    def _load_model(self, model_path):
        return AutoModelForCausalLM.from_pretrained(
            model_path,
            #model_file=model_file,
            #model_type="mistral",
            gpu_layers=50,
            stop=["<|im_end|>"],
            max_new_tokens=40,
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

    def update_ai_info(self, ai_name: str, ai_description: str, ai_first_message: str):
        """Updates AI name, description, and first message."""
        self.ai_name = ai_name
        self.ai_description = ai_description
        self.ai_first_message = ai_first_message

    def start_game(self):
        # Update ai_name for all users
        for user in self.users.values():
            user.ai_name = self.ai_name
            user.add_message(self.ai_description)
            user.add_message(self.ai_first_message)

    def send_message(self, user_id: int, message: str, generate = True):
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
    """Runs the AI."""# Create an instance of the Model class
    model = Model(ai_name="ChatGPT", ai_description="An AI chatbot", ai_first_message="Hello! How can I assist you today?")

    # Add a user
    user_id = 0
    model.add_user(user_name="Ethan", user_id=user_id)

    model.start_game()

    model.send_message(user_id, "Hellow cutie *winks*")