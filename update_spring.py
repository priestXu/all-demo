import os
import re
import fileinput


def replace_api_model_property_with_schema(file_path):
    # 用于匹配 @ApiModelProperty(value = "xxx") 或 @ApiModelProperty("xxx") 或 @ApiModelProperty(name = "xxx") 格式的正则表达式
    pattern_apimodel = r'@ApiModelProperty\s*\(\s*(?:value\s*=\s*["\']([^"\']*)["\']|["\']([^"\']*)["\']|name\s*=\s*[' \
                       r'"\']([^"\']*)["\'])\s*\)'

    # 用于替换的字符串
    replace_string_apimodel = r'@Schema(name="\1\2\3")'

    # 用于匹配 @ApiModel 或 @ApiModel("xxx") 或 @ApiModel(value = "xxx") 格式的正则表达式
    pattern_apimodel_decl = r'@ApiModel\s?\(\s*(?:value\s*=\s*["\']([^"\']*)["\']|["\']([^"\']*)["\']\s*\))?'

    # 用于替换的字符串
    replace_string_apimodel_decl = r'@Schema\(\)'

    # 用于匹配 io.swagger.annotations.ApiModelProperty 格式的正则表达式
    pattern_apimodel_import = r'import\s+io\.swagger\.annotations\.ApiModelProperty'

    # 用于匹配 io.swagger.annotations.ApiModelProperty 格式的正则表达式
    pattern_apimodel_import_2 = r'import\s+io\.swagger\.annotations\.ApiModel'

    # 用于替换的字符串
    replace_string_apimodel_import = r'import io.swagger.v3.oas.annotations.media.Schema'

    # 打开文件，逐行读取并替换内容
    with fileinput.FileInput(file_path, inplace=True, backup='.bak') as file:
        for line in file:
            line = re.sub(pattern_apimodel_decl, replace_string_apimodel_decl, line.rstrip())
            line = re.sub(pattern_apimodel, replace_string_apimodel, line.rstrip())
            line = re.sub(r'@ApiModel(?!\w)', '@Schema', line.rstrip())
            line = re.sub(pattern_apimodel_import, replace_string_apimodel_import, line.rstrip())
            line = re.sub(pattern_apimodel_import_2, replace_string_apimodel_import, line.rstrip())
            print(line)


def replace_api_operation_with_operation(file_path):
    # 用于匹配 @ApiOperation("xxx") 或 @ApiOperation(value="xxx") 或 @ApiOperation(value = "xxx", notes = "yyy") 格式的正则表达式
    pattern_apioperation = r'@ApiOperation\s*\(\s*(?:value\s*=\s*["\']([^"\']*)["\']\s*,\s*notes\s*=\s*["\']([' \
                           r'^"\']*)["\']|value\s*=\s*["\']([^"\']*)["\']|["\']([^"\']*)["\']\s*\s*)\s*\)'

    # 用于替换的字符串
    replace_string_apioperation = r'@Operation(summary="\1\2\3\4")'

    # 用于匹配 io.swagger.annotations.ApiOperation 格式的正则表达式
    pattern_apioperation_import = r'import\s+io\.swagger\.annotations\.ApiOperation'

    # 用于替换的字符串
    replace_string_apioperation_import = r'import io.swagger.v3.oas.annotations.Operation'

    # 打开文件，逐行读取并替换内容
    with fileinput.FileInput(file_path, inplace=True, backup='.bak') as file:
        for line in file:
            line = re.sub(pattern_apioperation, replace_string_apioperation, line.rstrip())
            line = re.sub(pattern_apioperation_import, replace_string_apioperation_import, line.rstrip())
            print(line)


def replace_api_param_with_parameter(file_path):
    # 用于匹配 @ApiParam("xxx") 或 @ApiParam(value="xxx") 格式的正则表达式
    pattern_apiparam_1 = r'@ApiParam\s*\(\s*(?:value\s*=\s*["\']([^"\']*)["\']\s*|["\']([^"\']*)["\']\s*\))'

    # 用于替换的字符串
    replace_string_apiparam_1 = r'@Parameter(description="\1\2")'

    # 用于匹配 @ApiParam(value = "xxx", required = true) 格式的正则表达式
    pattern_apiparam_2 = r'@ApiParam\s*\(.*value\s*=\s*["\']([^"\']*)["\'].*required\s*=\s*(true).*\)'

    # 用于替换的字符串
    replace_string_apiparam_2 = r'@Parameter(description="\1", required=\2)'

    # 用于匹配 io.swagger.annotations.ApiParam 格式的正则表达式
    pattern_apiparam_import = r'import\s+io\.swagger\.annotations\.ApiParam'

    # 用于替换的字符串
    replace_string_apiparam_import = r'import io.swagger.v3.oas.annotations.Parameter'

    # 打开文件，逐行读取并替换内容
    with fileinput.FileInput(file_path, inplace=True, backup='.bak') as file:
        for line in file:
            line = re.sub(pattern_apiparam_2, replace_string_apiparam_2, line.rstrip())
            line = re.sub(pattern_apiparam_1, replace_string_apiparam_1, line.rstrip())
            line = re.sub(pattern_apiparam_import, replace_string_apiparam_import, line.rstrip())
            print(line)


def replace_log_library(file_path):
    # 用于匹配 com.goodsogood.log4j2cm 格式的正则表达式
    pattern_log = r'com\.goodsogood\.log4j2cm'

    # 用于替换的字符串
    replace_string_log = r'com.aidangqun.log4j2cm'

    # 打开文件，逐行读取并替换内容
    with fileinput.FileInput(file_path, inplace=True, backup='.bak') as file:
        for line in file:
            line = re.sub(pattern_log, replace_string_log, line.rstrip())
            print(line)


def replace_api_with_tag(file_path):
    # 用于匹配 @Api(name = "XXX", tags = {"XXX"}) 或 @Api(name = "XXX", tags = ["XXX"]) 或 @Api(value = "XXX", tags = {"XXX"}) 格式的正则表达式
    pattern = r'@Api\s?\(\s?(?:name\s*=\s*["\']([^"\']*)["\']|value\s*=\s*["\']([^"\']*)["\'])(?:\s*,\s*tags\s*=\s*\{([^}]*)\}|\s*,\s*tags\s*=\s*\[([^]]*)\])\s*\)'

    # 用于替换的字符串
    replace_string = r'@Tag(name="\1\2\3\4")'

    # 打开文件，逐行读取并替换内容
    with fileinput.FileInput(file_path, inplace=True, backup='.bak') as file:
        for line in file:
            line = re.sub(pattern, replace_string, line.rstrip())
            print(line)

def replace_in_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.java') or file.endswith('.kt'):
                file_path = os.path.join(root, file)
                replace_api_operation_with_operation(file_path)
                replace_api_param_with_parameter(file_path)
                replace_log_library(file_path)
                replace_api_with_tag(file_path)
                replace_api_model_property_with_schema(file_path)

def delete_bak_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.bak'):
                file_path = os.path.join(root, file)
                os.remove(file_path)


if __name__ == "__main__":
    target_directory = "/Users/xuliduo/workspaces/IdeaProjects/ows-credit-center/src"
    replace_in_directory(target_directory)
    delete_bak_files(target_directory)
