#define L_Clk 2
#define Neg_Shift_Clk 3
#define Pos_Shift_Clk 4
#define Mas_RST 5
#define Neg_Srl_data 6
#define Pos_Srl_data 7


void setup() 
{
//  Serial.begin(9600);
  pinMode(L_Clk, OUTPUT);
  pinMode(Neg_Shift_Clk, OUTPUT);
  pinMode(Pos_Shift_Clk, OUTPUT);
  pinMode(Mas_RST, OUTPUT);
  pinMode(Neg_Srl_data, OUTPUT);
  pinMode(Pos_Srl_data, OUTPUT);

  
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

  
  digitalWrite(Mas_RST, LOW);
//  Serial.println("Mas_RST 10  LOW");
  delayMicroseconds(1);
  digitalWrite(Mas_RST, HIGH);
//  Serial.println("Mas_RST 10  HIGH");
  
  digitalWrite(8, HIGH);
  digitalWrite(9, HIGH);
  digitalWrite(10, HIGH);
  digitalWrite(11, HIGH);
  digitalWrite(12, HIGH);
  digitalWrite(13, HIGH);

  digitalWrite(Neg_Srl_data, HIGH);
  digitalWrite(Neg_Shift_Clk, HIGH);
  delayMicroseconds(1);
  digitalWrite(Neg_Shift_Clk, LOW);
  digitalWrite(L_Clk, HIGH);
  delayMicroseconds(1000);
  digitalWrite(L_Clk, LOW);
  digitalWrite(Neg_Srl_data, LOW);
}

int count = 0;
void loop() 
{
  if(count == 14)
  {
    count = 0; 
    digitalWrite(Neg_Srl_data, HIGH);
//    Serial.println("Neg_Srl_Data 14  HIGH");
    digitalWrite(Neg_Shift_Clk, HIGH);
    delayMicroseconds(1);
    digitalWrite(Neg_Shift_Clk, LOW);
    digitalWrite(Neg_Srl_data, LOW);
    digitalWrite(L_Clk, HIGH);
    delayMicroseconds(1);
    digitalWrite(L_Clk, LOW);
  }
  else
  {
    digitalWrite(Neg_Shift_Clk, HIGH);
    //  Serial.println("Neg_Shit_Clk 11  HIGH");
    delayMicroseconds(1);
    digitalWrite(Neg_Shift_Clk, LOW);
    //  Serial.println("Neg_Shit_Clk 11  LOW");
    digitalWrite(L_Clk, HIGH);
    //  Serial.println("L_Clk 12  HIGH");
    delayMicroseconds(1);
    digitalWrite(L_Clk, LOW);
    //  Serial.println("L_Clk 12  LOW");
  }
  count++;  
}
