#define col_byte 2    //Number of rows/8
#define col_num 6     //Number of columns

#define L_Clk 4
#define Neg_Shift_Clk 3
#define Pos_Shift_Clk 6
#define Mas_RST 5
#define Neg_Srl_data 2
#define Pos_Srl_data 7


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  pinMode(L_Clk, OUTPUT);
  pinMode(Neg_Shift_Clk, OUTPUT);
  pinMode(Pos_Shift_Clk, OUTPUT);
  pinMode(Mas_RST, OUTPUT);
  pinMode(Neg_Srl_data, OUTPUT);
  pinMode(Pos_Srl_data, OUTPUT);

  digitalWrite(Neg_Shift_Clk, LOW);
  digitalWrite(Pos_Shift_Clk, LOW);
  digitalWrite(L_Clk, LOW);

  
  digitalWrite(Mas_RST, LOW);
  delay(1);
  digitalWrite(Mas_RST, HIGH);

  digitalWrite(Pos_Srl_data, HIGH);
//  Serial.println("Pos_Srl_data, HIGH");
//  delayMicroseconds(1);
  digitalWrite(Pos_Shift_Clk, HIGH);
//  Serial.println("Pos_shift_clk, HIGH");
  delay(100);
  digitalWrite(Pos_Shift_Clk, LOW);
  digitalWrite(Pos_Srl_data, LOW);

}

void loop() {
  // put your main code here, to run repeatedly: 
//  char data_char[3] = {
  int data[col_byte + 1] = {0, 32, 0};
  int push = 0, temp;
  for(int i = 1; i <= col_byte; i++)
  {
    temp = 128;
    for(int j = 0; j < 8; j++)
    {
      push = data[i] & temp;
      push = push >> (7 - j);
      Serial.println(push);
      digitalWrite(Neg_Srl_data, push);
      digitalWrite(Neg_Shift_Clk, HIGH);
      delay(100);
      digitalWrite(Neg_Shift_Clk, LOW);
      temp = temp >> 1;
    }
  }
  digitalWrite(L_Clk, HIGH);
  delay(100);
  digitalWrite(L_Clk, LOW);
  digitalWrite(Pos_Shift_Clk, HIGH);
  delay(100);
  digitalWrite(Pos_Shift_Clk, LOW);
}
