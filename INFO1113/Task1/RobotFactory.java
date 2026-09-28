import java.util.Scanner;

public class RobotFactory {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        // Step 1: Get number of robots
        System.out.println("Enter number of robots:");
        int n = sc.nextInt();
        
        // Step 2: Declare arrays
        String[] serialNumbers = new String[n];
        int[] batteryLevels = new int[n];
        char[] errorCodes = new char[n];

        // Step 3: Input robot details with validation
        for (int i = 0; i < n; i++) {
            System.out.println("Enter details for robot " + (i + 1));

            // get serial number
            System.out.print("Enter serial number (6 characters): ");
            serialNumbers[i] = sc.next();
            if (serialNumbers[i].length() != 6) {
                System.out.println("Invalid serial number. Exiting program.");
                return;
            }

            // get battery level
            System.out.print("Enter battery level (0-100): ");
            
            batteryLevels[i] = sc.nextInt();
            if (batteryLevels[i] < 0 || batteryLevels[i] > 100) {
                System.out.println("Invalid battery level. Exiting program.");
                return;
            }

            // get error code
            System.out.print("Enter error code (N/W/E): ");
            String code = sc.next().toUpperCase();
            if (!(code.equals("N") || code.equals("W") || code.equals("E"))) {
                System.out.println("Invalid error code. Exiting program.");
                return;
            }
            errorCodes[i] = code.charAt(0);
        }

        // Step 4: Menu loop
        while (true) {
            System.out.println("Choose an analysis:");
            System.out.println("1. Print the average battery level");
            System.out.println("2. Print the total number of fully charged robots");
            System.out.println("3. Print the number of robots with error (E)");
            System.out.println("4. Print the serial number(s) of the robot(s) with the lowest battery");
            System.out.println("5. Search for a robot by serial number");
            System.out.println("6. Done");

            System.out.print("Your choice: ");
                        
            int choice = sc.nextInt();
        
            if (choice == 1){
                double average = HelperClass.averageBatteryLevel(batteryLevels);
                System.out.printf("Average battery level: %.2f%%\n", average);
            }
            else if (choice == 2){ 
                int fullyCharged = HelperClass.fullyChargedRobots(batteryLevels);
                System.out.println("Total fully charged robots: " + fullyCharged);
            }
            else if (choice == 3){
                int errors = HelperClass.countErrors(errorCodes);
                System.out.println("Robots with error (E): " + errors);
            }
            else if (choice == 4){
                HelperClass.lowestBatteryRobots(batteryLevels, serialNumbers);
            }
            else if (choice == 5) {
                System.out.print("Enter serial number to search: ");
                String search = sc.next();
                boolean found = HelperClass.searchRobot(serialNumbers, search);

                if (found)  System.out.println("Robot found");
                else        System.out.println("Robot not found");
            } 
            else{
                System.out.println("Exiting program.");
                return;
            }
        }
    }
}