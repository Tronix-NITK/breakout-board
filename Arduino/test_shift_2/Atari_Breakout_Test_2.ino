#define L_Clk 4
#define Neg_Shift_Clk 3
#define Pos_Shift_Clk 6
#define Mas_RST 5
#define Neg_Srl_data 2
#define Pos_Srl_data 7

void setup() 
{
  // put your setup code here, to run once:
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
  delayMicroseconds(1);
  digitalWrite(Mas_RST, HIGH);

  digitalWrite(Neg_Srl_data, HIGH);
  digitalWrite(Pos_Srl_data, HIGH);
  digitalWrite(Neg_Shift_Clk, HIGH);
  digitalWrite(Pos_Shift_Clk, HIGH);
  delay(100);
  digitalWrite(Neg_Shift_Clk, LOW);
  digitalWrite(Pos_Shift_Clk, LOW);
  digitalWrite(Neg_Srl_data, LOW);
  digitalWrite(Pos_Srl_data, LOW);

  digitalWrite(L_Clk, HIGH);
  delay(100);
  digitalWrite(L_Clk, LOW);
}


void loop() 
{
  // put your main code here, to run repeatedly:
  digitalWrite(Neg_Shift_Clk, HIGH);
  digitalWrite(Pos_Shift_Clk, HIGH);
  delay(100);
  digitalWrite(Neg_Shift_Clk, LOW);
  digitalWrite(Pos_Shift_Clk, LOW);
  
  digitalWrite(L_Clk, HIGH);
  delay(100);
  digitalWrite(L_Clk, LOW);
}
