# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
from http import HTTPStatus
import dashscope


def call_with_messages():
    messages = [{'role': 'system',
                 'content': '你是一个党建、党务业务专家，你对中国共产党的相关新闻也非常了解，后续我们会就这些进行聊天和问答。你也尽量只回答此类问题。'},
                {'role': 'user', 'content': '主题党日是什么呢？'}]

    response = dashscope.Generation.call(
        dashscope.Generation.Models.qwen_turbo,
        messages=messages,
        result_format='message',  # set the result to be "message" format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    call_with_messages()
