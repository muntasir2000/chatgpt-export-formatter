import argparse
import json
import logging
import sys

import preprocess


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()


def _save_to_sharegpt_format_json_file(conversations, output_file_path):
    with open(output_file_path, "w", encoding="utf8") as f_in:
        conversation_id = 0
        output_conversations = []
        for single_conversation in conversations:
            formatted_messages = []
            for message in single_conversation:
                if message[0] == "user":
                    formatted_messages.append({"from": "human", "value": message[1]})
                elif message[0] == "assistant":
                    formatted_messages.append({"from": "gpt", "value": message[1]})
                else:
                    logger.error("Got unexpected type of message from: %s", message[0])

            output_dict = {
                "id": f"{conversation_id}_0",
                "conversation": formatted_messages,
            }
            output_conversations.append(output_dict)
            conversation_id += 1

        f_in.write(json.dumps(output_conversations, ensure_ascii=False, indent=4, sort_keys=True))


def _process_file(input_chatgpt_json_path, output_file):
    logger.info("Loading input file: %s", input_chatgpt_json_path)
    logger.info("Output will be written to: %s", output_file)

    # need to load the entire file in memory, because it's only a single line json
    with open(input_chatgpt_json_path, encoding="utf8") as input_f:
        input_file_json = json.load(input_f)

    logger.info("Found %d conversations", len(input_file_json))
    result = preprocess.extract_conversations(input_file_json)
    _save_to_sharegpt_format_json_file(
        conversations=result,
        output_file_path=output_file,
    )
    
    logger.info("Done! Wrote %d conversations in %s", len(result), output_file)
    return result


def main():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument(
        "input_chatgpt_json",
        help="The path to the input json file from the ChatGPT export archive.",
    )
    parser.add_argument("output_file", help="The path to the output file.")

    args = parser.parse_args()

    _process_file(
        args.input_chatgpt_json,
        args.output_file,
    )


if __name__ == "__main__":
    main()
