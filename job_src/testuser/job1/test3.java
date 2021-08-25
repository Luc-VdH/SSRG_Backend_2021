
// Reversing an array using Java collections.
import java.util.*;
 
public class test3{
	public static void main(String [] args){
		reverse({1,2,3,4,5,6});
	}	 
    /*function reverses the elements of the array*/
    static void reverse(Integer a[])
    {
        Collections.reverse(Arrays.asList(a));
        System.out.println(Arrays.asList(a));
    }
 
    public static void main(String[] args)
    {
        Integer [] arr = {10, 20, 30, 40, 50};
        reverse(arr);
    }
}
