package com.dycjr.xiakuan;

import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.IllegalClassFormatException;
import java.security.ProtectionDomain;

public class MyClassTransformer implements ClassFileTransformer {

    @Override
    public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined,
            ProtectionDomain protectionDomain, byte[] classfileBuffer) throws IllegalClassFormatException {
        // TODO Auto-generated method stub
        return null;
    }
    
}
// import java.lang.instrument.ClassFileTransformer;
// import java.security.ProtectionDomain;

// import com.dycjr.xiakuan.feignagent.Constants;
// import com.dycjr.xiakuan.feignagent.EnableMyDiscovery;
// import com.dycjr.xiakuan.feignagent.utils.AnnotationUtil;
// import com.dycjr.xiakuan.feignagent.utils.ClassUtil;

// import javassist.CtClass;
// import javassist.CtMethod;
// import javassist.bytecode.AnnotationsAttribute;
// import javassist.bytecode.ClassFile;
// import javassist.bytecode.ConstPool;

// public class MyClassTransformer implements ClassFileTransformer {

//     static {
//         System.out.println("初始化, 添加不注册配置 =============> zookeeper.discovery.register = false");
//         System.setProperty("spring.cloud.zookeeper.discovery.register", "false");
//     }

//     @Override
//     public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined,
//             ProtectionDomain protectionDomain, byte[] classfileBuffer) {
//         try {
//             return transform0(loader, className, classBeingRedefined, protectionDomain, classfileBuffer);
//         } catch (Exception e) {
//             e.printStackTrace();
//         }
//         return null;
//     }

//     public byte[] transform0(ClassLoader loader, String className, Class<?> classBeingRedefined,
//             ProtectionDomain protectionDomain, byte[] classfileBuffer) {

//         if (className == null || !className.startsWith("com/dycjr")) {
//             return new byte[0];
//         }

//         CtClass clazz = ClassUtil.getClass(classfileBuffer);

//         if (clazz == null) {
//             return new byte[0];
//         }

//         ClassFile classFile = clazz.getClassFile();
//         ConstPool constPool = classFile.getConstPool();

//         boolean isChange = false;

//         // 如果是 spring boot app，则添加服务发现注解
//         // System.out.println("当前判定class =====================================> " + classFile.getName());
//         if (AnnotationUtil.anyContains(classFile, Constants.ANNOTATION_SPRING_BOOT_APP)) {
//             System.out.println("添加注解 ==========================================> @EnableMyDiscovery");
//             AnnotationUtil.addAnnotations(classFile, constPool, EnableMyDiscovery.class.getName());
//             isChange = true;
//         }
//         return toBytecode(clazz, isChange);
//     }

//     public static String getReturnType(CtMethod method) {
//         if (method == null) {
//             return null;
//         }

//         CtClass returnType = null;
//         try {
//             returnType = method.getReturnType();
//             return returnType.getName();
//         } catch (Exception e) {
//             System.out.println(e.getMessage());
//         }

//         return null;
//     }

//     public byte[] toBytecode(CtClass clazz, boolean isChange) {
//         if (clazz == null || !isChange) {
//             return new byte[0];
//         }
//         try {
//             System.out.println("===================change: "+ clazz.getName());
//             // 添加验证代码
//             System.out.println("当前类注解列表：" + clazz.getClassFile().getAttribute(AnnotationsAttribute.visibleTag));
//             return clazz.toBytecode();
//         } catch (Throwable e) {
//             System.out.println("toBytecode" + e.getMessage());
//         }
//         return new byte[0];
//     }

// }
