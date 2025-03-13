package com.dycjr.xiakuan.feigns.vos;

import lombok.Data;

import java.util.List;

@Data
public class FeignItem {
    
    private String name;

    private String status;

    private String statusTimestamp;

    private List<Instance> instances;
}
