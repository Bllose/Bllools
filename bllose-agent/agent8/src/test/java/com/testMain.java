package com;

import java.lang.management.MemoryMXBean;

public class testMain {
    public static void main(String[] args) {
        Runtime runtime = Runtime.getRuntime();
        System.out.println(String.format("剩余空间字节数 %d", runtime.freeMemory()));
        System.out.println(String.format("总内存的字节数 %d", runtime.totalMemory()));
        System.out.println(String.format("最大内存字节数 %d", runtime.maxMemory()));

        MemoryMXBean memoryMXBean = java.lang.management.ManagementFactory.getMemoryMXBean();
        System.out.println(memoryMXBean.getHeapMemoryUsage());
        System.out.println(memoryMXBean.getNonHeapMemoryUsage());
    }
}
