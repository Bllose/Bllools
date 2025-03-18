package com.dycjr.xiakuan;

import java.io.File;
import java.lang.instrument.Instrumentation;
import java.lang.reflect.Method;
import java.net.URL;
import java.net.URLClassLoader;

public class FeignAgent {
    
    public static void premain(String agentArgs, Instrumentation inst) {
        System.out.println("Bllose ==========================> agentArgs");
        inst.addTransformer(new MyClassTransformer());
        try {
            // 获取 Agent JAR 文件的路径
            URL agentJarUrl = FeignAgent.class.getProtectionDomain().getCodeSource().getLocation();
            File agentJarFile = new File(agentJarUrl.toURI());

            // 获取系统类加载器（通常是 URLClassLoader）
            ClassLoader systemClassLoader = ClassLoader.getSystemClassLoader();
            if (systemClassLoader instanceof URLClassLoader) {
                // 反射调用 addURL 方法
                URLClassLoader urlClassLoader = (URLClassLoader) systemClassLoader;
                Method addUrlMethod = URLClassLoader.class.getDeclaredMethod("addURL", URL.class);
                addUrlMethod.setAccessible(true); // 绕过访问权限检查
                addUrlMethod.invoke(urlClassLoader, agentJarFile.toURI().toURL());
                System.out.println("Agent JAR added to system classloader: " + agentJarFile);
            } else {
                System.err.println("System ClassLoader is not a URLClassLoader. Cannot add JAR.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        
    }
}
