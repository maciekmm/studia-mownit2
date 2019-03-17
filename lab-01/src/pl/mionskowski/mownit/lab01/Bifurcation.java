package pl.mionskowski.mownit.lab01;

public class Bifurcation {
    public static final float[] XS = new float[]{0.15f, 0.3f, 0.2435f, 0.9f, 0.421f};
    public static final float R_STEP = 0.00001f;
//    public static final float R_MIN = 1;
    public static final float R_MIN = 3.75f;
    public static final float R_MAX = 3.8f;
    public static final int ITERATIONS = 1 << 10;
    public static final int ITERATION_THRESHOLD = 1 << 3;
    public static final float DIFF_EPS = 0.00002f;

    public static void main(String[] args) {
        for (float r = R_MIN; r < R_MAX; r += R_STEP) {
            print(r, 0.4523f);
        }
    }

    public static void print(float r, float x) {
        for (int i = 0; i < ITERATIONS; i++) {
            if(x == Float.NEGATIVE_INFINITY || x== Float.POSITIVE_INFINITY) {
                return;
            }
//            if (i > ITERATION_THRESHOLD)
                System.out.println(String.format("%f\t%f", r, x));

            float nx = r * x * (1 - x);
            if (Math.abs(x - nx) < DIFF_EPS) {
                return;
            }

            x = nx;
        }
    }
}
