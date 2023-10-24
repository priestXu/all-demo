from http import HTTPStatus

from dashscope import Generation


def chatglmv2_call():
    prompt = '介绍下杭州'
    rsp = Generation.call(model='chatglm-6b-v2',
                          prompt=prompt,
                          history=[])
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        print(rsp.usage)
    else:
        print('Failed, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))


if __name__ == '__main__':
    chatglmv2_call()
