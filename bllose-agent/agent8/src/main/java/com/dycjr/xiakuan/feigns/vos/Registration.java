package com.dycjr.xiakuan.feigns.vos;

import lombok.Data;

@Data
public class Registration {
    private String name;

    private String managementUrl;

    private String healthUrl;

    // 用于请求的服务器地址
    private String serviceUrl;

    private String source;
}
