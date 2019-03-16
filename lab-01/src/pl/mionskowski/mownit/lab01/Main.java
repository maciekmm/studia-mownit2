package pl.mionskowski.mownit.lab01;

import java.util.function.Supplier;

public class Main {

    static int N = (int) Math.pow(10, 7);
    static float[] numbers = new float[N];
    static float FILL = 0.25214f;
    static final float expectedSum = FILL * N;

    public static void time(String name, Supplier<Float> runnable, float expectedSum) {
        long start = System.currentTimeMillis();
        FILL = (float) (Math.random() );
        for (int i = 0; i < numbers.length; i++) {
            numbers[i] = FILL;
        }
        float sum = runnable.get();

        long end = System.currentTimeMillis();
        System.out.println(FILL);
        if (Math.abs(expectedSum - sum) / FILL != 0f) {
            System.out.println("Found" + FILL);
        }

        System.out.println("Algorytm: " + name);
        System.out.println("Czas wykonania: " + (end - start) + "ms");
        System.out.println("Wynik: " + sum);
        System.out.println("Błąd bezwzględny: " + Math.abs(expectedSum - sum));
        System.out.println("Błąd względny: " + Math.abs(expectedSum - sum) / FILL);
//        System.out.println();
    }

    public static void main(String[] args) {
        for (int i = 0; i < numbers.length; i++) {
            numbers[i] = FILL;
        }
        // JVM warmup
        for (long i = 0; i < 100; i++) {
//            standardSum();
            time("Rekurencyjny", () -> recursiveSum(N), expectedSum);
        }
//        time("Standard", Main::standardSum, expectedSum);
//        time("Kahan", Main::kahan, expectedSum);
    }

    // Catastrophic cancellation
    // Niewielka zmiana na końcowych bitach mantysy
    // Dopełnione po normalizacji
    // Bardzo duzy błąd względny.
    public static float standardSum() {

        float sum = 0f;
        for (int i = 0; i < numbers.length; i++) {
            sum += numbers[i];
            if (i % 25000 == 0)
                System.out.println(i + "\t" + Math.abs(FILL * i - sum) / FILL);
        }

        return sum;

    }

    public static float kahan() {
        float sum = 0.0f;
        float err = 0.0f;
        for (int i = 0; i < numbers.length; ++i) {
            float y = numbers[i] - err;
            float temp = sum + y;
            err = (temp - sum) - y;
            sum = temp;
        }
        return sum;
    }

    public static float recursiveSum(int length) {
        while (length > 1) {
            for (int i = 0; i < length; i += 2) {
                if (i + 3 == length) {
                    numbers[i / 2] = numbers[i] + numbers[i + 1] + numbers[i + 2];
                    continue;
                }
                numbers[i / 2] = numbers[i] + numbers[i + 1];
            }
            length /= 2;
        }
        float sum = numbers[0] - FILL;
        return sum;
    }

}
