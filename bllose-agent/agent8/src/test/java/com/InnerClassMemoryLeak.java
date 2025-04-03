package com;

import java.util.ArrayList;
import java.util.List;

public class InnerClassMemoryLeak {
    private List<Object> data = new ArrayList<>();

    public static class InnerClass {
        public void doSomething() {
            // 使用外部类的 data
        }
    }

    public static void main(String[] args) {
        InnerClassMemoryLeak outer = new InnerClassMemoryLeak();
        InnerClass inner = new InnerClassMemoryLeak.InnerClass();
        // 后续 outer 不再使用，但 inner 仍然持有 outer 的引用
    }
}