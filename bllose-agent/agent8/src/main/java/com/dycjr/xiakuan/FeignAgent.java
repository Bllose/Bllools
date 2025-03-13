package com.dycjr.xiakuan;

import java.lang.instrument.Instrumentation;

public class FeignAgent {
    
    public static void premain(String agentArgs, Instrumentation inst) {
        System.out.println("Bllose ==========================> agentArgs");
        inst.addTransformer(new MyClassTransformer());
    }
}
