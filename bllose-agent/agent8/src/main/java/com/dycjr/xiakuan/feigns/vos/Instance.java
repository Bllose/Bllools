package com.dycjr.xiakuan.feigns.vos;

import lombok.Data;

@Data
public class Instance {
    
    private String id;

    private Integer version;

    private Boolean registered;

    private String statusTimestamp;

    private Registration registration;
}
