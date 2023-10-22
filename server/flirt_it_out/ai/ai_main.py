import multiprocessing
from ctransformers import AutoModelForCausalLM
import time


def run():
    model_id = "/home/ethan/flirt-it-out/server/flirt_it_out/ai/ai_models/mistral-7b-openorca.Q4_K_M.gguf"
    model_type = "mistral"
    stop = ["<|im_end|>"]

    def load_model():
        return AutoModelForCausalLM.from_pretrained(
            model_id,
            #model_file=model_file,
            model_type=model_type,
            gpu_layers=50,
            stop=stop,
            max_new_tokens=96,
            context_length=2048,
            local_files_only=True,
            threads=multiprocessing.cpu_count() - 2,
        )

    model = load_model()

    user_names = ["user0", "user1", "user2", "user3", "user4"]
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

    total_time = time.time()
    for user in user_names:
        start_time = time.time()
        generate = model(message_dict[user], stream=True)
        print(message_dict[user], end="", flush=True)
        for text in generate:
            print(text, end="", flush=True)
    print(time.time() - total_time)



def message_handler(message):
    return "Hello World!"
