package com.dycjr.xiakuan.discovery;

import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

@Configuration
@ComponentScan(basePackages = {"com.dycjr.xiakuan", "#{systemProperties['bllose.scan.packages']}"})
public class BaseScanPath {
    // 添加配置类初始化日志
    public BaseScanPath() {
        System.out.println("[Bllose Agent] 动态扫描路径已激活: " 
            + System.getProperty("bllose.scan.packages"));
    }
}
