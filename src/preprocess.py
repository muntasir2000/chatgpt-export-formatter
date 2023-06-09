import logging
from typing import List, Tuple, Dict, Any, Optional

logger = logging.getLogger()


def _is_valid_conversation(messages: List[Tuple[str, str]]) -> bool:
    """Determines if a conversation is valid. A conversation is valid if -
    - It has at least one human message and one assistant message.
    - The last message is from an assistant.
    - Each user turn only contains a single message

    Args:
        messages (List[Tuple[str, str]): List of messages of the conversation with
        in the following format - [("assistant", "hi there")]

    Returns:
        bool
    """
    # this loop will discard conversations with more than one user messages in a single turn
    expected_turn = "user"
    for message in messages:
        if message[0] != expected_turn:
            logger.info("Discarding conversation, unexptected turn im message.")
            return False

        if expected_turn == "user":
            expected_turn = "assistant"
        else:
            expected_turn = "user"

    if len(messages) < 2:
        logger.info("Discarding conversation due to very few messages.")
        return False
    if expected_turn == "assistant":
        logger.info(
            "Discarding conversation. No assistant response present for last message"
        )
        return False

    return True


def _is_valid_message(node: Optional[Dict[str, Any]]) -> bool:
    """
    Determines if a node represents a valid message.

    Args:
        node: A dictionary representing a node in a conversation.

    Returns:
        True if the node is a valid message; otherwise, False.
    """
    if node is None:
        return False

    message = node.get("message")
    if message is None:
        return False

    content = message.get("content")
    author = message.get("author")
    if content is None and author is None:
        return False

    if len(content.get("parts", [])) == 0:
        return False

    if len(content.get("parts")[0]) == 0:
        return False

    if content.get("content_type") != "text":
        return False

    if author.get("role") == "system":
        return False

    return True


def _get_conversation_messages(conversation: Dict[str, Any]) -> List[Tuple[str, str]]:
    """
    Extracts messages from a conversation.

    Args:
        conversation: A dictionary representing a conversation.

    Returns:
        A list of tuples where each tuple contains the author's role and the message.
    """
    messages = []
    current_node = conversation.get("current_node")

    while current_node is not None:
        node = conversation["mapping"].get(current_node)

        if _is_valid_message(node):
            author = node["message"]["author"]["role"]
            messages.append((author, node["message"]["content"]["parts"][0]))

        current_node = node.get("parent") if node else None

    return list(reversed(messages))


def extract_conversations(json_data: List[Dict[str, Any]]) -> List[List[Any]]:
    """
    Processes a list of conversations, extracting messages from each.

    Args:
        json_data: A list of dictionaries, each representing a conversation.

    Returns:
        A list of lists where each list contains a tuple for each message in a conversation.
        The tuple consists of the author's role and the message.
    """
    conversations = []
    for conversation in json_data:
        messages = _get_conversation_messages(conversation)
        if _is_valid_conversation(messages):
            conversations.append(messages)

    return conversations
