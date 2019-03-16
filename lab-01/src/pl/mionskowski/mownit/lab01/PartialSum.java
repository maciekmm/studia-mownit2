package pl.mionskowski.mownit.lab01;

public class PartialSum {
    public static final double[] S = new double[]{2, 3.6667f, 5, 7.2f, 10};
    public static final int[] N = new int[]{50, 100, 200, 500, 1000};


    public static void main(String[] args) {
        System.out.print('\t');
        for (int n : N) {
            System.out.print(n);
            System.out.print('\t');
        }
        System.out.println();
        if(false) {
            for (double s : S) {
                System.out.print(s);
                for (int n : N) {
                    System.out.print('\t');
                    float sum = dzeta((float) s, n, false);
                    float sum2 = dzeta((float) s, n, true);

                    double sub = sum2 - sum;
//                System.out.println("Różnica float: " + sub);
                    double sum3 = dzetaDouble((float) s, n, false);
                    double sum4 = dzetaDouble((float) s, n, true);

                    sub = sum4 - sum3;
                    System.out.print(sum4 - sum3);


//                System.out.println("Różnica double: " + sub);
                }
                System.out.println();
            }
        }

        for (double s : S) {
            System.out.print(s);
            for (int n : N) {
                System.out.print('\t');
                float sum = dirichletEta((float) s, n, false);
                float sum2 = dirichletEta((float) s, n, true);

                double sub = sum2 - sum;

                double sum3 = dirichletEtaDouble((float) s, n, false);
                double sum4 = dirichletEtaDouble((float) s, n, true);
                System.out.print(sum4-sum3);

                sub = sum4 - sum3;
            }
            System.out.println();
        }
    }

    public static float dzeta(float s, int n, boolean reverse) {
        float sum = 0f;
        if (!reverse) {
            for (int k = 1; k <= n; k++) {
                sum += 1 / (Math.pow(k, s));
            }
        } else {
            for (int k = n; k >= 1; k--) {
                sum += 1 / (Math.pow(k, s));
            }
        }
        return sum;
    }

    public static double dzetaDouble(double s, int n, boolean reverse) {
        double sum = 0f;
        if (!reverse) {
            for (int k = 1; k <= n; k++) {
                sum += 1 / (Math.pow(k, s));
            }
        } else {
            for (int k = n; k >= 1; k--) {
                sum += 1 / (Math.pow(k, s));
            }
        }
        return sum;
    }

    public static float dirichletEta(float s, int n, boolean reverse) {
        float sum = 0f;
        if (!reverse) {
            for (int k = 1; k <= n; k++) {
                sum += ((k % 2 == 0) ? -1 : 1) * 1 / (Math.pow(k, s));
            }
        } else {
            for (int k = n; k >= 1; k--) {
                sum += ((k % 2 == 0) ? -1 : 1) * 1 / (Math.pow(k, s));
            }
        }
        return sum;
    }

    public static double dirichletEtaDouble(double s, int n, boolean reverse) {
        double sum = 0f;
        if (!reverse) {
            for (int k = 1; k <= n; k++) {
                sum += ((k % 2 == 0) ? -1 : 1) * 1 / (Math.pow(k, s));
            }
        } else {
            for (int k = n; k >= 1; k--) {
                sum += ((k % 2 == 0) ? -1 : 1) * 1 / (Math.pow(k, s));
            }
        }
        return sum;
    }
}
