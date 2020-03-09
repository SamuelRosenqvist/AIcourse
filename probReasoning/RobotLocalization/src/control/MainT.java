package control;

import model.ProbLocalizer;
import view.RobotLocalizationViewer;

public class MainT {
	/*
	 * build your own if you like, this is just an example of how to start the viewer
	 * ...
	 */
	
	public static void main( String[] args) {
		
		/*
		 * generate you own localiser / estimator wrapper here to plug it into the 
		 * graphics class.
		 */
		ProbLocalizer l = new ProbLocalizer( 3, 3, 4);
  
		for(int i=0;i<3*3*4;i++){
			for(int j=0;j<3*3;j++){
				System.out.print(l.observationMatrices[i][j] + ", ");
			}	
			System.out.println("---");
		}   
 	}
}	