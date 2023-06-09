import argparse
import json
import logging
import sys

import preprocess

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()


def _save_to_samantha_format_jsonl_file(
    conversations, human_name, bot_name, output_file_path
):
    with open(output_file_path, "w", encoding="utf8") as f_in:
        elapsed_time = 0
        for single_conversation in conversations:
            formatted_messages = []
            for message in single_conversation:
                if message[0] == "user":
                    formatted_messages.append(f"{human_name}: {message[1]}")
                elif message[0] == "assistant":
                    formatted_messages.append(f"{bot_name}: {message[1]}")
                else:
                    logger.error("Got unexpected type of message from: {message[0]}")

            output_dict = {
                "elapsed": elapsed_time,
                "conversation": "\n\n".join(formatted_messages),
            }
            f_in.write(json.dumps(output_dict, ensure_ascii=False) + "\n")
            elapsed_time += 1


def _process_file(input_chatgpt_json_path, output_file, human_name, bot_name):
    logger.info("Loading input file: %s", input_chatgpt_json_path)
    logger.info("Output will be written to: %s", output_file)

    # need to load the entire file in memory, because it's only a single line json
    with open(input_chatgpt_json_path, encoding="utf8") as input_f:
        input_file_json = json.load(input_f)

    logger.info("Found %d conversations", len(input_file_json))
    result = preprocess.extract_conversations(input_file_json)
    _save_to_samantha_format_jsonl_file(
        conversations=result,
        human_name=human_name,
        bot_name=bot_name,
        output_file_path=output_file,
    )
    logger.info("Done! Wrote %d conversations in %s", len(result), output_file)


def main():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "--human-name",
        action="store",
        type=str,
        default="Theodore",
        help="Name of the human to use in the exported chat",
    )

    parser.add_argument(
        "--bot-name",
        action="store",
        type=str,
        default="Samantha",
        help="Name of the bot to use in the exported chat",
    )
    parser.add_argument(
        "input_chatgpt_json",
        help="The path to the input json file from the ChatGPT export archive.",
    )
    parser.add_argument("output_file", help="The path to the output file.")

    args = parser.parse_args()

    _process_file(
        args.input_chatgpt_json, args.output_file, args.human_name, args.bot_name
    )


if __name__ == "__main__":
    main()
