package com.dycjr.xiakuan.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.dycjr.xiakuan.Constants;

import javassist.CannotCompileException;
import javassist.ClassMap;
import javassist.ClassPool;
import javassist.CtClass;
import javassist.CtMethod;
import javassist.CtNewMethod;

public class MethodUtil {
    private static final Logger log = LoggerFactory.getLogger(MethodUtil.class);

    public static void beforeImport(CtClass clazz, String ...packages) {
        ClassPool classPool = clazz.getClassPool();
        if (classPool == null) {
            return;
        }
        for (String _package : packages) {
            classPool.importPackage(_package);
        }
    }

    public static CtMethod methodWrapper(CtClass clazz, CtMethod method, String code) {
        try {
            CtMethod copyMethod = CtNewMethod.copy(method, clazz, new ClassMap());

            // 旧方法重新命名
            String methodName = method.getName();
            method.setName(methodName + Constants.METHOD_RENAME_SUFFIX);

            StringBuffer body = new StringBuffer("{\n").append(code).append("\n}");

            // 设置新方法的名称和代码
            copyMethod.setName(methodName);
            copyMethod.setBody(body.toString());

            clazz.addMethod(copyMethod);

            return copyMethod;
        } catch (CannotCompileException e) {
            log.error("Copy method error.", e);
        }
        return null;
    }
}
