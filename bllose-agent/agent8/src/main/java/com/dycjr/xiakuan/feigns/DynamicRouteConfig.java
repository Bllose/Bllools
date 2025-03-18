package com.dycjr.xiakuan.feigns;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

import io.micrometer.core.instrument.util.StringUtils;

@Configuration
@ConfigurationProperties(prefix = "feign.dynamic-routes")
@Primary
public class DynamicRouteConfig {

    @Autowired
    private SpringBootAdmin springBootAdmin;

    private String env;

    // 服务名与URL映射表 示例：xk-order2: http://10.51.5.9:30019
    private Map<String, String> routeMapping = new ConcurrentHashMap<>();

    public String getTargetUrl(String serviceName) {
        return routeMapping.get(serviceName);
    }

    public void updateRoute(String serviceName, String newUrl) {
        routeMapping.put(serviceName, newUrl);
    }

    public void refreshRoutes(String env) {
        if(StringUtils.isBlank(env)) env = "test6";
        this.env = env;
        // 从SpringBootAdmin获取最新的路由信息
        Map<String, String> newRoutes = springBootAdmin.getHttpAddressByEnv(env);
        if(newRoutes.isEmpty()) return;

        // 更新路由映射表
        routeMapping.clear();
        routeMapping.putAll(newRoutes);
    }

    public String curEnvironment() {
        return this.env;
    }
}


