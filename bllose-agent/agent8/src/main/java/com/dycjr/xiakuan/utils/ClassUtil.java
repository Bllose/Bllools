package com.dycjr.xiakuan.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javassist.ClassPool;
import javassist.CtClass;

public class ClassUtil {
    private static final Logger log = LoggerFactory.getLogger(ClassUtil.class);

    public static CtClass getClass(String className) {
        ClassPool pool = ClassPool.getDefault();

        CtClass clazz = null;

        String name = className.replaceAll("/", ".");

        // 暂不支持内部类
        if (name.contains("$$")) {
            return null;
        }

        try {
            // 需要 com.xxx.xxx 形式才能获取
            clazz = pool.get(name);
        } catch (Throwable e) {
            log.error("Class not found: {}", name);
        }
        return clazz;
    }
}
