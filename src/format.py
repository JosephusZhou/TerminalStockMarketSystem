#!/usr/bin/python3


# 高亮内容
def format_light_content(content):
    return "\033[1;36m{s}\033[0m".format(s=str(content))


# 涨跌颜色
def format_up_down_content(up_down, content):
    if up_down == 1:
        return format_red_content(content)
    elif up_down == -1:
        return format_green_content(content)
    else:
        return content


# 涨
def format_red_content(content):
    return "\033[1;31m{s}\033[0m".format(s=str(content))


# 跌
def format_green_content(content):
    return "\033[1;32m{s}\033[0m".format(s=str(content))
