package com;

public interface MyInterface {
    public static final Integer value = 1;

    default int getValue() {
        return value;
    }

    public static int getValue2() {
        return value;
    }
}
