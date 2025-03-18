package com.dycjr.xiakuan.feigns;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import com.alibaba.fastjson.JSONObject;
import com.dycjr.xiakuan.feigns.vos.FeignItem;
import com.dycjr.xiakuan.feigns.vos.Instance;
import com.dycjr.xiakuan.feigns.vos.Registration;

@Component
public class SpringBootAdmin {
    private static final String ADMIN_URL = "https://aurora-admin.tclpv.cn";
    private final RestTemplate restTemplate;

    public SpringBootAdmin(@Qualifier("feignRestTemplate") RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    // 等效于Python的get_jsessionid方法
    public String getJsessionId(String env) {
        String loginUrl = UriComponentsBuilder.fromHttpUrl(ADMIN_URL)
                .pathSegment(env, "login")
                .queryParam("username", "admin")
                .queryParam("password", "admin123")
                .queryParam("remember-me", "on")
                .toUriString();

        HttpHeaders headers = new HttpHeaders();
        headers.setAll(new HashMap<String, String>() {{
            put("User-Agent", "Apifox/1.0.0 (https://apifox.com)");
            put("Referer", ADMIN_URL + "/" + env + "/login?username=admin&password=admin123&remember-me=on");
            }});

        ResponseEntity<String> response = restTemplate.exchange(
                loginUrl,
                HttpMethod.POST,
                new HttpEntity<>(headers),
                String.class);

        List<String> cookies = response.getHeaders().get(HttpHeaders.SET_COOKIE);
        try {
            return cookies.stream()
                    .filter(c -> c.startsWith("JSESSIONID="))
                    .map(c -> c.split(";")[0].split("=")[1])
                    .findFirst()
                    .orElse("");
        } catch (Exception e) {
            return "";
        }
    }

    // 等效于Python的get_server_info方法
    public String getServerInfo(String env, String jsessionId) {
        String apiUrl = UriComponentsBuilder.fromHttpUrl(ADMIN_URL)
                .pathSegment(env, "applications")
                .toUriString();

        HttpHeaders headers = new HttpHeaders();
        headers.set(HttpHeaders.COOKIE, "JSESSIONID=" + jsessionId);
        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));

        return restTemplate.exchange(
                apiUrl,
                HttpMethod.GET,
                new HttpEntity<>(headers),
                String.class).getBody();
    }

    // 等效于Python的get_http_address_by_env方法
    public Map<String, String> getHttpAddressByEnv(String env) {
        String jsessionId = getJsessionId(env);
        if(StringUtils.isEmpty(jsessionId)){
            return new HashMap<>();
        }
        String jsonResponse = getServerInfo(env, jsessionId);
        // 需要根据实际JSON结构实现解析逻辑
        return parseServiceUrls(jsonResponse);
    }
    
    private Map<String, String> parseServiceUrls(String json) {
        Map<String, String> hostHolder = new HashMap<>();

        List<FeignItem> feignItems = JSONObject.parseArray(json, FeignItem.class);
        for(FeignItem item : feignItems) {
            if ("UP".equals(item.getStatus())) {
                List<Instance> instances = item.getInstances();
                for (Instance instance : instances) {
                    if (instance.getRegistered()) {
                        Registration registration = instance.getRegistration();
                        hostHolder.put(registration.getName(), registration.getServiceUrl());
                    }
                }
            }
        }
        return hostHolder;
    }
}