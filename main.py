import colorama
from colorama import Fore

from regspam import pkmain

Flag = True

title = """
                                                                                                           
  ****           *                                                        ***** ***                 **    
 *  *************                                                      ******  * **                  **   
*     *********                                                       **   *  *  **                  **   
*     *  *                                                           *    *  *   **                  **   
 **  *  **                    ***    ***                  ****           *  *    *                   **   
    *  ***            ***    * ***  **** *     ****      * **** *       ** **   *       ***      *** **   
   **   **           * ***      *** *****     * ***  *  **  ****        ** **  *       * ***    ********* 
   **   **          *   ***      ***  **     *   ****  ****             ** ****       *   ***  **   ****  
   **   **         **    ***      ***       **    **     ***            ** **  ***   **    *** **    **   
   **   **         ********      * ***      **    **       ***          ** **    **  ********  **    **   
    **  **         *******      *   ***     **    **         ***        *  **    **  *******   **    **   
     ** *      *   **          *     ***    **    **    ****  **           *     **  **        **    **   
      ***     *    ****    *  *       *** * **    **   * **** *        ****      *** ****    * **    **   
       *******      *******  *         ***   ***** **     ****        *  ****    **   *******   *****     
         ***         *****                    ***   **               *    **     *     *****     ***      
                                                                     *                                    
                                                                      **                                  
 by 4ozRabclip                                                                                       
                                                                                                          
                                                                                                          
"""

def menu():
    while Flag:
        colorama.init()
        print(Fore.RED + title)
        print(Fore.WHITE)
        print("1. Registration Flood (aka Phishkiller)\n")
        print("2. Reverse Shell\n")
        choice = input("Select: ")

        if choice == "1":
            print("\n")
            pkmain(return_to_menu)

def return_to_menu():
    print("\033[H\033[J")  
    menu()





if __name__ == '__main__':
    menu()