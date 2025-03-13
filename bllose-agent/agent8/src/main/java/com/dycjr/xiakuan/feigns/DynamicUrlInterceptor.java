package com.dycjr.xiakuan.feigns;

import feign.RequestInterceptor;
import feign.RequestTemplate;
import io.micrometer.core.instrument.util.StringUtils;

public class DynamicUrlInterceptor implements RequestInterceptor {
    private final DynamicRouteConfig routeConfig;
    private String apolloEnv = "test6";

    public DynamicUrlInterceptor(DynamicRouteConfig routeConfig, String apolloEnv) {
        this.apolloEnv = apolloEnv;
        this.routeConfig = routeConfig;
    }

    @Override
    public void apply(RequestTemplate template) {
        String serviceName = template.feignTarget().name();
        routeConfig.refreshRoutes(apolloEnv);
        String targetUrl = routeConfig.getTargetUrl(serviceName);
        
        if (StringUtils.isNotBlank(targetUrl)) {
            template.target(targetUrl);
            System.out.println("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓");
            System.out.println(String.format("Dynamic routing - service: %s -> %s (%s)", serviceName, targetUrl, routeConfig.curEnvironment()));
            System.out.println("↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑");
        } else {
            System.out.println("↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓");
            System.out.println(String.format("Dynamic routing - service: %s -> %s (%s)", serviceName, "No target url", routeConfig.curEnvironment()));
            System.out.println("↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑");
        }
    }
}