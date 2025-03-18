package com.dycjr.xiakuan;

import java.lang.instrument.ClassFileTransformer;
import java.lang.instrument.IllegalClassFormatException;
import java.security.ProtectionDomain;

import org.objectweb.asm.AnnotationVisitor;
import org.objectweb.asm.ClassReader;
import org.objectweb.asm.ClassVisitor;
import org.objectweb.asm.MethodVisitor;
import org.objectweb.asm.Opcodes;  // This is the correct import
import org.objectweb.asm.Type;

public class MyClassTransformer implements ClassFileTransformer {

    static {
        System.out.println("初始化, 添加不注册配置 =============> zookeeper.discovery.register = false");
        System.setProperty("spring.cloud.zookeeper.discovery.register", "false");

        System.out.println("初始化, 测试环境数据库 =============> db.mysql = jdbc:mysql://10.51.2.157:3306");
        System.setProperty("db.mysql", "jdbc:mysql://10.51.2.157:3306");
        System.setProperty("spring.datasource.password", "OALUQXWciJouw8ydeok=");
    }

    @Override
    public byte[] transform(ClassLoader loader, String className, 
                          Class<?> classBeingRedefined, ProtectionDomain protectionDomain,
                          byte[] classfileBuffer) throws IllegalClassFormatException {
            if(className != null && className.contains("com/dycjr/xiakuan/order/XkOrderApplication")) {
                System.out.println("Bllose ================================> 开始分析: " + className);
                try{
                ClassReader reader = new ClassReader(classfileBuffer);
                MyClassVisitor visitor = new MyClassVisitor(Opcodes.ASM9);
                reader.accept(visitor, 0);
            }catch(Exception e){
                e.printStackTrace();
            }
        }
        return null;
    }
    
}

class MyClassVisitor extends ClassVisitor {
    public MyClassVisitor(int api) {
        super(api);
    }

    // 新增：获取类级别注解
    @Override
    public AnnotationVisitor visitAnnotation(String descriptor, boolean visible) {
        System.out.println("类注解: " + descriptor.replace('/', '.'));
        
        // 示例：处理特定注解（如@SpringBootApplication）
        if ("Lorg/springframework/boot/autoconfigure/SpringBootApplication;".equals(descriptor)) {
            return new AnnotationVisitor(Opcodes.ASM9) {
                @Override
                public void visit(String name, Object value) {
                    // 处理注解属性（如scanBasePackages）
                    if ("scanBasePackages".equals(name)) {
                        System.out.println("scanBasePackages: " + value);
                    }
                    super.visit(name, value);
                }
            };
        }
        return super.visitAnnotation(descriptor, visible);
    }

    @Override
    public void visit(int version, int access, String name, 
                    String signature, String superName, String[] interfaces) {
        // 收集父类和接口
        System.out.println("父类: " + superName.replace('/', '.'));
        for (String itf : interfaces) {
            System.out.println("接口: " + itf.replace('/', '.'));
        }
        super.visit(version, access, name, signature, superName, interfaces);
    }

    @Override
    public MethodVisitor visitMethod(int access, String name, String descriptor,
                                    String signature, String[] exceptions) {
        // 收集方法抛出的异常
        if (exceptions != null) {
            for (String ex : exceptions) {
                System.out.println("异常类: " + ex.replace('/', '.'));
            }
        }
        return new MethodVisitor(Opcodes.ASM9) {
            @Override
            public void visitFieldInsn(int opcode, String owner, String name, String descriptor) {
                // 收集字段类型
                Type type = Type.getType(descriptor);
                System.out.println("字段类型: " + type.getClassName());
            }

            @Override
            public void visitMethodInsn(int opcode, String owner, String name, 
                                    String descriptor, boolean isInterface) {
                // 收集方法调用类
                System.out.println("方法调用类: " + owner.replace('/', '.'));
                Type[] argTypes = Type.getArgumentTypes(descriptor);
                for (Type t : argTypes) {
                    System.out.println("参数类型: " + t.getClassName());
                }
            }
        };
    }
}