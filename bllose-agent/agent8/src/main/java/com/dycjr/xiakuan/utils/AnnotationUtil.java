package com.dycjr.xiakuan.utils;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Optional;
import java.util.Set;

import javassist.CtMethod;
import javassist.bytecode.AnnotationsAttribute;
import javassist.bytecode.AttributeInfo;
import javassist.bytecode.ClassFile;
import javassist.bytecode.ConstPool;
import javassist.bytecode.annotation.Annotation;

public class AnnotationUtil {

    public static boolean addAnnotations(ClassFile classFile, ConstPool constPool, String ...annotations) {
        if (classFile == null || constPool == null) {
            System.out.println("addAnnotations: classFile or constPool is null.");
            return false;
        }

        if (annotations.length == 0) {
            System.out.println("addAnnotations: annotations is empty, class: " + classFile.getName());
            return false;
        }

        AnnotationsAttribute annotationsAttribute = getVisibleAnnotationsAttribute(classFile)
                .orElse(new AnnotationsAttribute(constPool, AnnotationsAttribute.visibleTag));
        if (annotationsAttribute == null) {
            System.out.println("addAnnotations: class " +classFile.getName()+ "'s annotationsAttribute is null." );
            return false;
        }

        for (String annotation : annotations) {
            javassist.bytecode.annotation.Annotation agentAnnotation =
                new javassist.bytecode.annotation.Annotation(annotation, constPool);

            annotationsAttribute.addAnnotation(agentAnnotation);
        }

        classFile.addAttribute(annotationsAttribute);
        System.out.println(String.format("addAnnotations: successfully, %s, %s", classFile.getName(), String.join(",", annotations)));
        return true;
    }

    public static boolean addAnnotations(CtMethod method, String ...annotations) {
        if (method == null) {
            System.out.println("addAnnotations: method is null.");
            return false;
        }

        if (annotations.length == 0) {
            System.out.println(String.format("addAnnotations: annotations is empty, methods: %s.", method.getName()));
            return false;
        }

        ConstPool constPool = method.getMethodInfo().getConstPool();

        if (constPool == null) {
            System.out.println(String.format("addAnnotations: method %s's constPool is null.", method.getName()));
            return false;
        }

        AnnotationsAttribute annotationsAttribute = getVisibleAnnotationsAttribute(method)
                .orElse(new AnnotationsAttribute(constPool, AnnotationsAttribute.visibleTag));
        if (annotationsAttribute == null) {
            System.out.println(String.format("addAnnotations: method %s's annotationsAttribute is null.", method.getName()));
            return false;
        }

        for (String annotation : annotations) {
            javassist.bytecode.annotation.Annotation agentAnnotation =
                new javassist.bytecode.annotation.Annotation(annotation, constPool);

            annotationsAttribute.addAnnotation(agentAnnotation);
        }

        method.getMethodInfo().addAttribute(annotationsAttribute);
        System.out.println(String.format("addAnnotations: successfully, %s, %s", method.getName(), String.join(",", annotations)));
        return true;
    }

    public static boolean removeAnnotations(ClassFile classFile, ConstPool constPool, String ...annotations) {
        if (classFile == null || constPool == null) {
            System.out.println("removeAnnotations: classFile or constPool is null.");
            return false;
        }

        AnnotationsAttribute annotationsAttribute = getVisibleAnnotationsAttribute(classFile).orElse(null);
        if (annotationsAttribute == null) {
            System.out.println("removeAnnotations: annotationsAttribute is null.");
            return false;
        }

        boolean isUpdate = false;

        AnnotationsAttribute updateAnnotationsAttribute = new AnnotationsAttribute(constPool, AnnotationsAttribute.visibleTag);

        Set<String> removeAnnotations = new HashSet<>();
        removeAnnotations.addAll(Arrays.asList(annotations));

        Set<String> doneSet = new HashSet<>();

        for (Annotation annotation : annotationsAttribute.getAnnotations()) {
            // 过滤需要移除的注解
            if (removeAnnotations.contains(annotation.getTypeName())) {
                isUpdate = true;
                doneSet.add(annotation.getTypeName());
                continue;
            }
            // 不需删除的注解拷贝到新的注解属性
            updateAnnotationsAttribute.addAnnotation(annotation);
        }

        // 更新注解
        if (isUpdate) {
            classFile.addAttribute(updateAnnotationsAttribute);
        }

        System.out.println(String.format("removeAnnotations: successfully, %s, %s", classFile.getName(), String.join(",", doneSet)));

        return isUpdate;
    }

    public static boolean removeAnnotations(CtMethod method, String ...annotations) {
        if (method == null || method.getMethodInfo() == null ||  method.getMethodInfo().getConstPool() == null) {
            System.out.println("removeAnnotations: method, methodInfo or constPool is null.");
            return false;
        }

        ConstPool constPool = method.getMethodInfo().getConstPool();

        AnnotationsAttribute annotationsAttribute = getVisibleAnnotationsAttribute(method).orElse(null);
        if (annotationsAttribute == null) {
            System.out.println("removeAnnotations: annotationsAttribute is null.");
            return false;
        }

        boolean isUpdate = false;

        AnnotationsAttribute updateAnnotationsAttribute = new AnnotationsAttribute(constPool, AnnotationsAttribute.visibleTag);

        Set<String> removeAnnotations = new HashSet<>();
        removeAnnotations.addAll(Arrays.asList(annotations));

        Set<String> doneSet = new HashSet<>();

        for (Annotation annotation : annotationsAttribute.getAnnotations()) {
            // 过滤需要移除的注解
            if (removeAnnotations.contains(annotation.getTypeName())) {
                isUpdate = true;
                doneSet.add(annotation.getTypeName());
                continue;
            }
            // 不需删除的注解拷贝到新的注解属性
            updateAnnotationsAttribute.addAnnotation(annotation);
        }

        // 更新注解
        if (isUpdate) {
            method.getMethodInfo().addAttribute(updateAnnotationsAttribute);
        }

        System.out.println(String.format("removeAnnotations: successfully, %s, %s", method.getName(), String.join(",", doneSet)));

        return isUpdate;
    }

    public static boolean allContains(ClassFile classFile, String ...annotations) {
        if (classFile == null) {
            return false;
        }

        AnnotationsAttribute annotationsAttribute = getVisibleAnnotationsAttribute(classFile).orElse(null);
        if (annotationsAttribute == null) {
            return false;
        }

        for (String annotation : annotations) {
            if (annotationsAttribute.getAnnotation(annotation) == null) {
                return false;
            }
        }

        return true;
    }

    public static boolean anyContains(ClassFile classFile, String ...annotations) {
        if (classFile == null) {
            return false;
        }

        AnnotationsAttribute annotationsAttribute = getVisibleAnnotationsAttribute(classFile).orElse(null);
        if (annotationsAttribute == null) {
            return false;
        }

        // any contains
        for (String annotation : annotations) {
            if (annotationsAttribute.getAnnotation(annotation) != null) {
                return true;
            }
        }

        return false;
    }

    public static boolean anyContains(CtMethod method, String ...annotations) {
        if (method == null) {
            return false;
        }

        AnnotationsAttribute annotationsAttribute = getVisibleAnnotationsAttribute(method).orElse(null);
        if (annotationsAttribute == null) {
            return false;
        }

        // any contains
        for (String annotation : annotations) {
            if (annotationsAttribute.getAnnotation(annotation) != null) {
                return true;
            }
        }

        return false;
    }

    public static Optional<AnnotationsAttribute> getVisibleAnnotationsAttribute(ClassFile classFile) {
        if (classFile == null) {
            return Optional.empty();
        }

        AttributeInfo attributeInfo = classFile.getAttribute(AnnotationsAttribute.visibleTag);
        if (attributeInfo == null || !(attributeInfo instanceof AnnotationsAttribute)) {
            return Optional.empty();
        }

        return Optional.of((AnnotationsAttribute) attributeInfo);
    }

    public static Optional<AnnotationsAttribute> getVisibleAnnotationsAttribute(CtMethod method) {
        if (method == null || method.getMethodInfo() == null) {
            return Optional.empty();
        }

        AttributeInfo attributeInfo = method.getMethodInfo().getAttribute(AnnotationsAttribute.visibleTag);
        if (attributeInfo == null || !(attributeInfo instanceof AnnotationsAttribute)) {
            return Optional.empty();
        }

        return Optional.of((AnnotationsAttribute) attributeInfo);
    }

}
