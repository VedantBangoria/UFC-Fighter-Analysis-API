package ufcAPI;

import java.util.Arrays;

public class DetailPackage {
    private String ref;
    private double[] stats;
    private String fighter1;
    private String fighter2;

    public DetailPackage(String ref, double[] stats, String f1, String f2) {
        this.ref = ref;
        this.stats = stats;
        this.fighter1 = f1;
        this.fighter2 = f2;
    }

    public String toString() {
        return "{ref : " + ref + ", fighters :" + fighter1 + "," + fighter2 +
        ", stats : " + Arrays.toString(stats) + "}";
    }

    public String getRef() {
        return ref;
    }

    

    public double[] getStats() {
        return stats;
    }

    

    public String getFighter1() {
        return fighter1;
    }

    

    public String getFighter2() {
        return fighter2;
    }

    

    

}