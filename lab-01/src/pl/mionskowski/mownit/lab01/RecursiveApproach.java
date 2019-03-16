package pl.mionskowski.mownit.lab01;

public class RecursiveApproach {
    public static void main(String[] args) {
        for (float x = 0; x < 1f; x += Math.random()/1000)
            print(4f, x);
    }

    public static final float min = 0.000000002f;

    public static void print(float r, float x) {
        float nx = x;
        long max = 20000000;
        long it = 0;
        while (nx != 0 && it < max && Math.abs(nx) > min) {
            nx = r * nx * (1 - nx);
            it++;
        }
        if(it != max)
            System.out.println(String.format("%f\t%d", x, it));
    }
}
