public class HelperClass{
    // returns the average battery level
    public static double averageBatteryLevel(int[] batteryLevels){
        double total = 0;
        for (int i = 0; i<batteryLevels.length; i++) {
            total += batteryLevels[i];
        }
        double avg = total / batteryLevels.length;
        return avg;
    }

    // returns the total number of fully charged robots
    public static int fullyChargedRobots(int[] batteryLevels){
        int count = 0;
        for (int i = 0; i<batteryLevels.length; i++) {
            if (batteryLevels[i] == 100) {
                count++;
            }
        }
        return count;
    }
    
    // returns the total number of robots with error code 'E'
    public static int countErrors(char[] errorCodes){
        int count = 0;
        char check = 'E';
        for (int i = 0; i<errorCodes.length; i++) {
            if (errorCodes[i] == check) {
                count++;
            }
        }
        return count;
    }

    // prints the serial number of the robots with lowest battery level
    public static void lowestBatteryRobots(int[] batteryLevels, String[] serialNumbers){
        //find the lowest battery level
        int lowest = 100;
        for (int i = 0; i<batteryLevels.length; i++) {
            if (batteryLevels[i] <= lowest) {
                lowest = batteryLevels[i];
            }
        }
        String[] arr = new String[batteryLevels.length];
        for (int i = 0; i<batteryLevels.length; i++) {
            if (batteryLevels[i] == lowest) {
                arr[i] = serialNumbers[i];
            }
        }
        //print the serial numbers of the robots with lowest battery level
        System.out.println("Serial number(s) with lowest battery:");
        for (int i = 0; i<batteryLevels.length; i++) {
            if (arr[i] != null) {
                System.out.println(arr[i]);
            }
        }
        
    }

    // returns whether the robot with the given serial number exists in the array 
    public static boolean searchRobot(String[] serialNumbers, String search){
        if (serialNumbers == null || search == null) return false;
        for (int i = 0; i < serialNumbers.length; i++) {
            if (serialNumbers[i] != null && search.equalsIgnoreCase(serialNumbers[i].trim())) {
                return true;
            }
        }
        return false;
    }
}