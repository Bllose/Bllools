package com.dycjr.xiakuan.feigns;

import feign.Client;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Value;

@Configuration(value = "myFeignConfig")
@EnableConfigurationProperties(DynamicRouteConfig.class)
public class FeignConfig {

    @Value("${apollo.env:test6}")
    private String apolloEnv;

    private final DynamicRouteConfig routeConfig;

    public FeignConfig(DynamicRouteConfig routeConfig) {
        this.routeConfig = routeConfig;
    }

    private String logo = 
            "/_/\\     /_____/\\ /_____/\\ /_______/\\ /________/\\/_______/\\/_____/\\ /__/\\ /__/\\     /_______/\\ /_____/\\ /_____/\\ /_/\\     /_/\\     /_____/\\     \n" +
            "\\:\\ \\    \\:::_ \\ \\\\:::__\\/ \\::: _  \\ \\\\__.::.__\\/\\__.::._\\/\\:::_ \\ \\\\::\\_\\\\  \\ \\    \\::: _  \\ \\\\:::_ \\ \\\\:::_ \\ \\\\:\\ \\    \\:\\ \\    \\:::_ \\ \\    \n" +
            " \\:\\ \\    \\:\\ \\ \\ \\\\:\\ \\  __\\::(_)  \\ \\  \\::\\ \\     \\::\\ \\  \\:\\ \\ \\ \\\\:. `-\\  \\ \\    \\::(_)  \\ \\\\:(_) \\ \\\\:\\ \\ \\ \\\\:\\ \\    \\:\\ \\    \\:\\ \\ \\ \\   \n" +
            "  \\:\\ \\____\\:\\ \\ \\ \\\\:\\ \\/_/\\\\:: __  \\ \\  \\::\\ \\    _\\::\\ \\__\\:\\ \\ \\ \\\\:. _    \\ \\    \\:: __  \\ \\\\: ___\\/ \\:\\ \\ \\ \\\\:\\ \\____\\:\\ \\____\\:\\ \\ \\ \\  \n" +
            "   \\:\\/___/\\\\:\\_\\ \\ \\\\:\\_\\ \\ \\\\:.\\ \\  \\ \\  \\::\\ \\  /__\\::\\__/\\\\:\\_\\ \\ \\\\. \\`-\\  \\ \\    \\:.\\ \\  \\ \\\\ \\ \\    \\:\\_\\ \\ \\\\:\\/___/\\\\:\\/___/\\\\:\\_\\ \\ \\ \n" +
            "    \\_____\\/ \\_____\\/ \\_____\\/ \\__\\/\\__\\/   \\__\\/  \\________\\/ \\_____\\/ \\__\\/ \\__\\/     \\__\\/\\__\\/ \\_\\/     \\_____\\/ \\_____\\/ \\_____\\/ \\_____\\/ \n" +
            "                                                                                                        current env: ${{env}}";

    @Bean
    public DynamicUrlInterceptor dynamicUrlInterceptor() {
        System.out.println("\n\n");
        System.out.println(logo.replace("${{env}}", apolloEnv));
        System.out.println("\n");
        return new DynamicUrlInterceptor(routeConfig, apolloEnv);
    }

    @Bean
    public Client feignClient(@Qualifier("feignRestTemplate") RestTemplate restTemplate) {
        return new Client.Default(null, null);
    }
}
