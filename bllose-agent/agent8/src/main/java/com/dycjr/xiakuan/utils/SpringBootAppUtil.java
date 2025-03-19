package com.dycjr.xiakuan.utils;

import java.util.ArrayList;
import java.util.List;

import javassist.bytecode.ClassFile;

public class SpringBootAppUtil {
    private static final List<String> beanAnnotaions = new ArrayList<>();

    static {
        beanAnnotaions.add("org.springframework.context.annotation.Configuration");
        beanAnnotaions.add("org.springframework.stereotype.Component");
        beanAnnotaions.add("org.springframework.stereotype.Service");
        beanAnnotaions.add("org.springframework.stereotype.Controller");
        beanAnnotaions.add("org.springframework.stereotype.Repository");
        beanAnnotaions.add("org.springframework.web.bind.annotation.ControllerAdvice");
        beanAnnotaions.add("org.springframework.web.bind.annotation.RestController");
        beanAnnotaions.add("org.springframework.web.bind.annotation.RestControllerAdvice");
    }

    public static boolean isBeanClass(ClassFile classFile) {
        return AnnotationUtil.anyContains(classFile, beanAnnotaions.toArray(new String[0]));
    }
}
