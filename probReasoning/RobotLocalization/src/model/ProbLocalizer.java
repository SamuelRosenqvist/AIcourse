package model;

import control.EstimatorInterface;
import java.util.Random;

public class ProbLocalizer implements EstimatorInterface {
		
    private int rows, cols, head;
    private int[] trueState; // x,y,h  where heading is 0,1,2,3 = n,e,s,w
    private int[] sensorState;
    private double[][] transitionMatrix;
    private double[][] transposedTM;
    public double[][] observationMatrices;  //rows*cols+1 nr of observation matrices stored as column vectors
    private double[][] fMatrix;
    private boolean sensorSuccess;
    private Random Prand = new Random(); 
    private double totalDist;
    private int iterations;
    //private boolean initFlag;

	public ProbLocalizer( int rows, int cols, int head) {
		this.rows = rows;
		this.cols = cols;
		this.head = head;
        this.trueState = new int[3];
        this.sensorState = new int[2];
        this.transitionMatrix = new double[rows*cols*4][rows*cols*4];
        this.transposedTM = new double[rows*cols*4][rows*cols*4];
        this.observationMatrices = new double[rows*cols*4][rows*cols];
        this.fMatrix = new double[rows*cols*4][rows*cols*4];
        this.totalDist = 0;
        this.iterations = 0;
        //this.initFlag = false;

        Random rand = new Random(); 
        int start_x = rand.nextInt(rows); 
        int start_y = rand.nextInt(cols); 
        int start_h;
        if       (start_x==0 && start_y==0){
            start_h = 1+rand.nextInt(2);
        } else if(start_x==0 && start_y==cols){
            start_h = rand.nextInt(2);
        } else if(start_x==rows && start_y==0){
            start_h = 2+rand.nextInt(2);
        } else if(start_x==rows && start_y==cols){
            start_h = (3+rand.nextInt(2)) % 4;
        } else if(start_x==0){
            start_h = rand.nextInt(3);
        } else if(start_x==rows){
            start_h = (2+rand.nextInt(3)) % 4;
        } else if(start_y==0){
            start_h = 1+rand.nextInt(3);
        } else if(start_y==cols){
            start_h = (3+rand.nextInt(3)) % 4;
        } else {
            start_h = rand.nextInt(head);
        }
        this.trueState[0] = start_x;
        this.trueState[1] = start_y;
        this.trueState[2] = start_h; 

        for(int i =0;i<=rows*cols*4-1;i++){
                fMatrix[i][i]=(double)1/(rows*cols*4);
        }
        init();
    }	
    
    
    private void init(){
        int row = rows-1;
        int col = cols-1;
        // fill in the transitionMatrix
        for(int r=0; r<rows; r++){
            for(int c=0; c<cols ; c++ ){
                if((r==0 || r==row) && (c==0|| c==col)){
                    fillCorner(r,c);
                } else if((r==0 || r==row) || (c==0|| c==col)){
                    fillSide(r,c);
                } else {
                    fillMiddle(r,c);
                }
            }
        }

        for(int i = 0; i<rows*cols*4;i++){
            for(int j = 0; j<rows*cols*4;j++){
                transposedTM[j][i]=transitionMatrix[i][j];
            }
        }

        // fill in the observation matrices
        for(int r = 0 ; r<rows; r++){
            for(int c = 0 ; c<cols; c++){
                for(int h = 0; h<=3; h++){

                    for(int nr=0;nr <rows; nr++){
                        for(int nc=0;nc<cols;nc++){
                            if(r==nr && c==nc){
                                observationMatrices[(r*cols*4+c*4+h)][(nr*cols)+nc] = 0.1;
                            } else if(is1Neighbour(r,c,nr,nc)){
                                observationMatrices[(r*cols*4+c*4+h)][(nr*cols)+nc] = 0.05;
                            } else if(is2Neighbour(r,c,nr,nc)){
                                observationMatrices[(r*cols*4+c*4+h)][(nr*cols)+nc] = 0.025;
                            }
                        }
                    }
                }
            }
        }
    }

    private boolean is1Neighbour(int r, int c, int nr, int nc){
        if(Math.abs(r-nr)<=1 && Math.abs(c-nc)<=1){
            return true;
        } else {
            return false;
        }
    }

    private boolean is2Neighbour(int r, int c, int nr, int nc){
        if( (Math.abs(r-nr)<=2 &&  Math.abs(c-nc)<=2)){
            return true;
        } else {
            return false;
        }
    }

    private double nothingProb(int r, int c){
        double sum = 0.0;
        double[] temp = observationMatrices[r*cols+c];
        for (double v : temp){
            sum += v;
        }
        return (1-sum);
    }

    private void fillCorner(int r,int c){
        int row = rows-1;
        int col = cols-1;
        if(r==0 && c==0){
            fillTile(r, c, 0, r, c+1, 1, .5);
            fillTile(r, c, 0, r+1, c, 2, .5);

            fillTile(r, c, 1, r, c+1, 1, .7);
            fillTile(r, c, 1, r+1, c, 2, .3);

            fillTile(r, c, 2, r, c+1, 1, .3);
            fillTile(r, c, 2, r+1, c, 2, .7);

            fillTile(r, c, 3, r, c+1, 1, .5);
            fillTile(r, c, 3, r+1, c, 2, .5);
        } else if (r==0 && c==col){
            fillTile(r, c, 0, r, c-1, 3, .5);
            fillTile(r, c, 0, r+1, c, 2, .5);

            fillTile(r, c, 1, r, c-1, 3, .5);
            fillTile(r, c, 1, r+1, c, 2, .5);

            fillTile(r, c, 2, r, c-1, 3, .3);
            fillTile(r, c, 2, r+1, c, 2, .7);

            fillTile(r, c, 3, r, c-1, 3, .7);
            fillTile(r, c, 3, r+1, c, 2, .3);
        } else if (r==row && c==0){
            fillTile(r, c, 0, r-1, c, 0, .7);
            fillTile(r, c, 0, r, c+1, 1, .3);

            fillTile(r, c, 1, r-1, c, 0, .3);
            fillTile(r, c, 1, r, c+1, 1, .7);

            fillTile(r, c, 2, r-1, c, 0, .5);
            fillTile(r, c, 2, r, c+1, 1, .5);

            fillTile(r, c, 3, r-1, c, 0, .5);
            fillTile(r, c, 3, r, c+1, 1, .5);
        } else if (r==row && c==col){
            fillTile(r, c, 0, r-1, c, 0, .7);
            fillTile(r, c, 0, r, c-1, 3, .3);

            fillTile(r, c, 1, r-1, c, 0, .5);
            fillTile(r, c, 1, r, c-1, 3, .5);
            
            fillTile(r, c, 2, r-1, c, 0, .5);
            fillTile(r, c, 2, r, c-1, 3, .5);
            
            fillTile(r, c, 3, r-1, c, 0, .3);
            fillTile(r, c, 3, r, c-1, 3, .7);
        }
    }

    private void fillSide(int r,int c){
        double p0 =0;
        double p1 =0;
        double p2 =0;
        double p3 =0;
        int row = rows-1;
        int col = cols-1;
        if(r==0){
            for(int h=0;h<=3;h++){
                if(h==0){
                    p1 = 0.33;
                    p2 = 0.33;
                    p3 = 0.33;
                } else if(h == 1){
                    p1=0.7;
                    p2=0.15;
                    p3=0.15;
                }else if(h == 2){
                    p1=0.15;
                    p2=0.7;
                    p3=0.15;
                }else if(h == 3){
                    p1=0.15;
                    p2=0.15;
                    p3=0.7;
                }
                fillTile(r, c, h, r, c-1, 3, p3);
                fillTile(r, c, h, r, c+1, 1, p1);
                fillTile(r, c, h, r+1, c, 2, p2);
            }
        } else if (r==row){
            for(int h=0;h<=3;h++){
                if(h==0){
                    p0=0.7;
                    p1=0.15;
                    p3=0.15;
                } else if(h == 1){
                    p0=0.15;
                    p1=0.7;
                    p3=0.15;
                }else if(h == 2){
                    p0 = 0.33;
                    p1 = 0.33;
                    p3 = 0.33;
                }else if(h == 3){
                    p0=0.15;
                    p1=0.15;
                    p3=0.7;
                }
                fillTile(r, c, h, r, c-1, 3, p3);
                fillTile(r, c, h, r, c+1, 1, p1);
                fillTile(r, c, h, r-1, c, 0, p0);
            }
        } else if (c==0){
            for(int h=0;h<=3;h++){
                if(h==0){
                    p0=0.7;
                    p1=0.15;
                    p2=0.15;
                } else if(h == 1){
                    p0=0.15;
                    p1=0.7;
                    p2=0.15;
                }else if(h == 2){
                    p0 = 0.15;
                    p1 = 0.15;
                    p2 = 0.7;
                }else if(h == 3){
                    p0=0.33;
                    p1=0.33;
                    p2=0.33;
                }
                fillTile(r, c, h, r-1, c, 0, p0);
                fillTile(r, c, h, r+1, c, 2, p2);
                fillTile(r, c, h, r, c+1, 1, p1);
            }
        } else if (c==col){
            for(int h=0;h<=3;h++){
                if(h==0){
                    p0=0.7;
                    p2=0.15;
                    p3=0.15;
                } else if(h == 1){
                    p0=0.33;
                    p2=0.33;
                    p3=0.33;
                }else if(h == 2){
                    p0=0.15;
                    p2=0.7;
                    p3=0.15;
                }else if(h == 3){
                    p0=0.15;
                    p2=0.15;
                    p3=0.7;
                }
                fillTile(r, c, h, r-1, c, 0, p0);
                fillTile(r, c, h, r+1, c, 2, p2);
                fillTile(r, c, h, r, c-1, 3, p3);
            }
        }
    }

    private void fillMiddle(int r,int c){
        double p0 = 0;
        double p1 = 0;
        double p2 = 0;
        double p3 = 0;
        for(int h=0;h<=3;h++){
            if(h==0){
                p0 = 0.7;
                p1 = 0.1;
                p2 = 0.1;
                p3 = 0.1;
            } else if(h == 1){
                p0 =0.1;
                p1 =0.7;
                p2 =0.1;
                p3 =0.1;
            }else if(h == 2){
                p0 =0.1;
                p1 =0.1;
                p2 =0.7;
                p3 =0.1;
            }else if(h == 3){
                p0 =0.1;
                p1 =0.1;
                p2 =0.1;
                p3 =0.7;
            }
            fillTile(r, c, h, r-1, c, 0, p0);
            fillTile(r, c, h, r, c+1, 1, p1);
            fillTile(r, c, h, r+1, c, 2, p2);
            fillTile(r, c, h, r, c-1, 3, p3);
        }
    }

    private void fillTile(int r, int c, int h, int nr, int nc , int nh, double p){
        transitionMatrix[(r*cols*4)+c*4+h][nr*cols*4+nc*4+nh]=p;
    }


	public int getNumRows() {
		return rows;
	}
	
	public int getNumCols() {
		return cols;
	}
	
	public int getNumHead() {
		return head;
	}
	
	public double getTProb( int x, int y, int h, int nX, int nY, int nH) {
        return transitionMatrix[x*cols*4+y*4+h][nX*cols*4+nY*4+nH];
	}

	public double getOrXY( int rX, int rY, int x, int y, int h) {
        if(rX == -1 || rY == -1){
            return 0.6;
        }
        //System.out.println("getOrXY " + rX +" "+ rY +" "+ x +" "+ y +" "+ h);
		return observationMatrices[x*cols*4+y*4+h][rX*cols+rY];
	}


	public int[] getCurrentTrueState() {
		int x=trueState[0];
        int y=trueState[1];
        int h=trueState[2];
        int[] state = new int[3];
        state[0]=x;
        state[1]=y;
        state[2]=h;
        return state;
	}

	public int[] getCurrentReading() {
        if(sensorSuccess){
            return sensorState;
        } else {
            return null;
        }
	}


	public double getCurrentProb( int x, int y) {
        double p = 0;
        for(int i = 0; i<=3; i++){
            for(int j=0;j<rows*cols*4;j++){
                p += fMatrix[x*cols*4+y*4+i][j];
            }
            //p += fMatrix[x*cols*4+y*4+i][x*cols*4+y*4+i];
        }
        return p;
	}
	
	public void update() {
        iterations++;
        moveBot();
        double rd = Prand.nextDouble();
        double q_nothing = nothingProb(trueState[0], trueState[1]);
        if(rd<=q_nothing){
            sensorSuccess=false;
        } else {
            sensorSuccess=true;
            setSensorState();
        }

        int[] sens = sensorState;
        int x = sens[0];
        int y = sens[1];
        double[] obsR = observationMatrices[x*cols*4+y*4+head-1];
        double[][] obsM = new double[rows*cols*4][rows*cols*4];
        for(int i = 0; i<rows*cols; i++){
            for(int j = 0; j<4;j++){
                obsM[i*head+j][i*head+j] = obsR[i];
            }
        }
 
        // forward step
        fMatrix = alpha(mMult(mMult(obsM,transposedTM),fMatrix));
        manhattanEval();
        double averageDist = totalDist/iterations;
        System.out.println("Average distance: " + averageDist + "  Iteration: " + iterations);
        // fmatrix
        /* for(int i=0;i<fMatrix.length;i++){
            for(int j=0;j<fMatrix[0].length;j++){
                System.out.print(fMatrix[i][j] + " ");
            }	
            System.out.println("---"); 
        } */
        // probabilities
        /* 
        for(int i=0;i<rows;i++){
            for(int j=0;j<rows;j++){
                System.out.print(getCurrentProb(i, j) + " ");
            }	
            System.out.println("---");
        }    */
    }

    private double[][] alpha(double[][] M){
        double sum = 0;
        for (int i = 0; i < rows*cols*4; i++){
            for (int j = 0; j < rows*cols*4; j++){
                sum += M[i][j];
            }  
        }
        for (int i = 0; i < rows*cols*4; i++){
            for (int j = 0; j < rows*cols*4; j++){
                M[i][j] = 2*M[i][j]/sum;
            }  
        }
        return M;
    }


    private double[][] mMult(double[][] A, double[][] B){
        int aRows = A.length;
        int aColumns = A[0].length;
        int bRows = B.length;
        int bColumns = B[0].length;

        if (aColumns != bRows) {
            throw new IllegalArgumentException("Dimension mismatch.");
        }

        double[][] C = new double[aRows][bColumns];

        for (int i = 0; i < aRows; i++) { // aRow
            for (int j = 0; j < bColumns; j++) { // bColumn
                for (int k = 0; k < aColumns; k++) { // aColumn
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
        return C;
    }
	
    private void moveBot(){
        int[] tS = trueState;
        int x = tS[0];
        int y = tS[1];
        int h = tS[2];
        double[][] potentialPos = new double[cols*rows*4][4];

        RandomCollection<double[]> rc = new RandomCollection<double[]>();
        for(int i = 0; i<cols*rows*4; i++){
            if(transitionMatrix[x*cols*4+y*4+h][i]!=(double)0.0){
                int temp = i;//x*cols*4+y*4+h;
                potentialPos[i][2]=temp%4;
                potentialPos[i][1]=((temp-temp%4)/head)%cols;
                potentialPos[i][0]=(temp-potentialPos[i][2]-4*potentialPos[i][1])/(head*cols);
                potentialPos[i][3]=transitionMatrix[x*cols*4+y*4+h][i];
                rc.add(potentialPos[i][3], potentialPos[i]);
            }
        }

        double[] nextPos = rc.next();
        trueState[0]=(int)nextPos[0];
        trueState[1]=(int)nextPos[1];
        trueState[2]=(int)nextPos[2];
    }
    
    private void setSensorState(){
        int[] tS = trueState;
        int x = tS[0];
        int y = tS[1];
        int h = tS[2];
        double[][] obsRow = new double[rows*cols][3];
        RandomCollection<double[]> rc = new RandomCollection<double[]>();

        for(int i = 0; i<cols*rows; i++){
            if(observationMatrices[x*cols*4+y*4+h][i]!=(double)0.0){
                obsRow[i][0]=(i-(i%cols))/cols;
                obsRow[i][1]=i-obsRow[i][0]*cols;
                obsRow[i][2]=observationMatrices[x*cols*4+y*4+h][i];
                rc.add(obsRow[i][2],obsRow[i]);
            }
        }

        double[] nextPos = rc.next();
        sensorState[0]=(int)nextPos[0];
        sensorState[1]=(int)nextPos[1];
    }

    private void manhattanEval(){
        double max = 0;
        int x = -1;
        int y = -1;  
        for(int i=0;i<rows;i++){
            for(int j=0;j<rows;j++){
                if(max<getCurrentProb(i, j)){
                    max=getCurrentProb(i, j);
                    x=i;
                    y=j;
                }
            }	
        }    

        int tx = trueState[0];
        int ty = trueState[1];
        int dist = Math.abs(tx-x)+Math.abs(ty-y);
        //System.out.println("Manhattan dist: " + dist);
        totalDist+=dist;
    }
}