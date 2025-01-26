from enum import Enum


class FileStatus(Enum):
    NOT_UPLOADED = 0
    UPLOADING = 1
    UPLOADED_OR_CONVERTED_HTML = 2
    UPLOAD_FAILED = 3
    WAITING_FOR_PDF_CONVERSION = 4
    CONVERTED_PDF = 5
    ADDING_WATERMARK = 6
    WATERMARK_ADDED = 7
    PDF_CONVERSION_IN_PROGRESS = 8
    PDF_CONVERSION_FAILED = 9
    WAITING_FOR_HTML_CONVERSION = 10
    HTML_CONVERSION_IN_PROGRESS = 11
    HTML_CONVERSION_FAILED = 12

    # 手动定义一个映射，将枚举值和对应的描述信息关联起来
    _msg_map = {
        NOT_UPLOADED: "文件未上传",
        UPLOADING: "文件上传中",
        UPLOADED_OR_CONVERTED_HTML: "文件上传已完成 或 文件已转换（HTML）",
        UPLOAD_FAILED: "文件上传失败",
        WAITING_FOR_PDF_CONVERSION: "文件等待转换（PDF）",
        CONVERTED_PDF: "文件已转换（PDF）",
        ADDING_WATERMARK: "加水印中",
        WATERMARK_ADDED: "加水印完毕",
        PDF_CONVERSION_IN_PROGRESS: "文件转化中（PDF）",
        PDF_CONVERSION_FAILED: "文件转换失败（PDF）",
        WAITING_FOR_HTML_CONVERSION: "文件等待转换（HTML）",
        HTML_CONVERSION_IN_PROGRESS: "文件转换中（HTML）",
        HTML_CONVERSION_FAILED: "文件转换失败（HTML）"
    }

    @property
    def msg(self):
        return self._msg_map.value[self.value]

    @classmethod
    def from_code(cls, code):
        for member in cls:
            if member.value == code:
                return member
        raise ValueError(f"Invalid code: {code}")


# 示例使用
def get_status_message(code):
    try:
        status = FileStatus.from_code(code)
        return status.msg
    except ValueError as e:
        return str(e)


if __name__ == '__main__':
    # 测试
    print(get_status_message(1))  # 输出: 文件上传中
    print(get_status_message(2))  # 输出: 文件上传已完成 或 文件已转换（HTML）
    print(get_status_message(13))  # 输出: Invalid code: 13