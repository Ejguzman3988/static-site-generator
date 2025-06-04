from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


PARAGRAPH = BlockType.PARAGRAPH
HEADING = BlockType.HEADING
CODE = BlockType.CODE
QUOTE = BlockType.QUOTE
UNORDERED_LIST = BlockType.UNORDERED_LIST
ORDERED_LIST = BlockType.ORDERED_LIST


def block_to_block_type(md_block):
    is_block_type = [
        is_ordered_list_block,
        is_unordered_list_block,
        is_quote_block,
        is_code_block,
        is_heading,
    ]

    block_type = PARAGRAPH

    for func in is_block_type:
        block_type = func(md_block)
        if block_type != PARAGRAPH:
            break

    return block_type


def is_ordered_list_block(block_str):
    if len(block_str) < 3:
        return PARAGRAPH

    is_ordered_list = True

    count = 0
    for line in block_str.split("\n"):
        count += 1
        find_dot = line.find(".")
        prefix = line[:find_dot]

        if (
            len(line) < 3
            or find_dot < 1
            or not prefix.isnumeric()
            or int(prefix) != count
            or len(line) <= find_dot + 2
            or line[find_dot + 1] != " "
            or not line[find_dot + 2].isalnum()
        ):

            is_ordered_list = False
            break

    return ORDERED_LIST if is_ordered_list else PARAGRAPH


def is_unordered_list_block(block_str):
    if len(block_str) < 2:
        return PARAGRAPH
    is_unordered_list = True
    for line in block_str.split("\n"):
        if len(line) < 2 or line[0] != "-" or line[1] != " ":
            is_unordered_list = False
            break
    return UNORDERED_LIST if is_unordered_list else PARAGRAPH


def is_quote_block(block_str):
    is_quote = True
    for line in block_str.split("\n"):
        if line[0] != ">":
            is_quote = False
            break
    return QUOTE if is_quote else PARAGRAPH


def is_code_block(block_str):
    return (
        len(block_str) > 6 and CODE
        if len(block_str) > 6 and block_str[:3] == "```" and block_str[-3:] == "```"
        else PARAGRAPH
    )


def is_heading(block_str):
    count = 0
    for index in range(len(block_str)):
        char = block_str[index]
        if char == "#" and count != 6:
            count += 1
        else:
            break
    return (
        HEADING
        if (len(block_str) >= (count + 2))
        and block_str[count] == " "
        and block_str[count + 1].isalnum()
        else PARAGRAPH
    )


def block_to_str(block_str):
    return " ".join(block_str.split("\n"))
