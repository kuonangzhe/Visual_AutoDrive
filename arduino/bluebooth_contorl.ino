#include <Servo.h>   
#define SER1_BAUD 9600
/*电机驱动引脚*/
#define PWMB_IN1  11       //定义IN1引脚
#define PWMB_IN2 6       //定义IN2引脚
#define PWMA_IN1 5        //定义IN3引脚
#define PWMA_IN2 3        //定义IN4引脚
#define Servor_Pin    7
#define  BEEP_PIN    12             //定义蜂鸣器引脚D6
#define  NLED_PIN    13           //定义呼吸灯引脚D11
#define  NLED_MS_BETWEEN        500
#define  DUOJI_MS_BETWEEN       20.000
String uart1_receive_buf = "";   //声明一个字符串数组
int pwm_value=1500;
char flag_x=0;
char flag_y=0;
char flag_z=0;
char  sign=1;
char val=0;
char Flag=0;
Servo myservo;           //创建舵机伺服对象数组
#define Forward  1
#define Back     2
#define Left     3
#define Right    4
char dir1=0;
char dir2=0;
unsigned char handle_ms_between( unsigned long *time_ms, unsigned int ms_between);
void handle_nled();
void dida(u8 times, u8 frequency);
void Motor_Forward(char motor,char pwm);
void Motor_Left(char motor,char pwm);
void Motor_Right(char motor,char pwm);
void Motor_Turn_Left(char motor,char pwm);
void Motor_Turn_Right(char motor,char pwm);
void Motor_Stop(char motor);
void Motor_Back(char motor,char pwm);
void handle_uart1();
void setup() {
   pinMode(BEEP_PIN, OUTPUT);
   pinMode(NLED_PIN, OUTPUT);; 
   Serial.begin(SER1_BAUD); 
   myservo.attach(Servor_Pin);
   myservo.writeMicroseconds(1500);
   dida(1, 1000);
   delay(1000);
}

void loop() {
        
  handle_uart1();
}

unsigned char handle_ms_between( unsigned long *time_ms, unsigned int ms_between) {
    if(millis() - *time_ms < ms_between) {
        return 0;  
    } else{
         *time_ms = millis();
         return 1;
    }
}
void handle_nled() {
    static unsigned long systick_ms_bak = 0;
    if(!handle_ms_between(&systick_ms_bak, NLED_MS_BETWEEN))return;  
    digitalWrite(NLED_PIN, val);
    val = ~val;
}
void dida(u8 times, u8 frequency) {
    for(byte i = 0; i < times; i++ ) {
        digitalWrite(BEEP_PIN, LOW);
        delay(frequency);
        delay(frequency);
        digitalWrite(BEEP_PIN, HIGH );
        delay(frequency);
        delay(frequency);  
    }
}

void Motor_Forward(char motor,char pwm)
{
  if(motor==1)
  {
      digitalWrite(PWMA_IN1,HIGH );
      digitalWrite(PWMA_IN2,LOW );
     //analogWrite(PWMA_IN1,pwm);
     //analogWrite(PWMA_IN2,255);
  }
  else if(motor==2)
  {
      digitalWrite(PWMB_IN1,HIGH );
      digitalWrite(PWMB_IN2,LOW );
     //analogWrite(PWMB_IN1,pwm);
    // analogWrite(PWMB_IN2,255); 
  }
}

void Motor_Back(char motor,char pwm)
{
  if(motor==1)
  {
      digitalWrite(PWMA_IN1,LOW);
      digitalWrite(PWMA_IN2,HIGH );
    // analogWrite(PWMA_IN1,255);
    // analogWrite(PWMA_IN2,pwm);
  }
  else if(motor==2)
  {
      digitalWrite(PWMB_IN1,LOW );
      digitalWrite(PWMB_IN2,HIGH );
    // analogWrite(PWMB_IN1,255);
    // analogWrite(PWMB_IN2,pwm); 
  }
}

void Motor_Right(char motor,char pwm)
{
    if(motor==1)
  {
     analogWrite(PWMA_IN1,pwm);
     analogWrite(PWMA_IN2,255);
  }
  else if(motor==2)
  {
     analogWrite(PWMB_IN1,255);
     analogWrite(PWMB_IN2,255); 
  }
}
void Motor_Left(char motor,char pwm)
{
    if(motor==1)
  {
     analogWrite(PWMA_IN1,255);
     analogWrite(PWMA_IN2,255);
  }
  else if(motor==2)
  {
     analogWrite(PWMB_IN1,pwm);
     analogWrite(PWMB_IN2,255); 
  }
}

void Motor_Turn_Right(char motor,char pwm)
{
    if(motor==1)
  {
     analogWrite(PWMA_IN1,pwm);
     analogWrite(PWMA_IN2,255);
  }
  else if(motor==2)
  {
     analogWrite(PWMB_IN1,255);
     analogWrite(PWMB_IN2,pwm); 
  }
}

void Motor_Turn_Left(char motor,char pwm)
{
    if(motor==1)
  {
     analogWrite(PWMA_IN1,255);
     analogWrite(PWMA_IN2,pwm);
  }
  else if(motor==2)
  {
     analogWrite(PWMB_IN1,pwm);
     analogWrite(PWMB_IN2,255); 
  }
}
void Motor_Stop(char motor)
{
    if(motor==1)
  {
      digitalWrite(PWMA_IN1,LOW );
      digitalWrite(PWMA_IN2,LOW );
    // analogWrite(PWMA_IN1,255);
    // analogWrite(PWMA_IN2,255);
  }
  else if(motor==2)
  {
      digitalWrite(PWMB_IN1,LOW );
      digitalWrite(PWMB_IN2,LOW );
    // analogWrite(PWMB_IN1,255);
     //analogWrite(PWMB_IN2,255); 
  }
}


void handle_uart1() {
    static unsigned int index=0, time1=0, pwm=0, i;
    static char get_ok = 0, get_byte;
    unsigned int len;
    while(Serial.available())  {      //如果串口有数据
         get_byte = char(Serial.read());
        uart1_receive_buf  += get_byte;
        delay(5);      
    }
    
    
    //Serial.println(uart1_receive_buf);
   
    if((uart1_receive_buf[0] =='<') && (uart1_receive_buf[1] =='S'))
          {   
          
            if((uart1_receive_buf[2] =='U') && (uart1_receive_buf[3] =='P')) index=1;
            if((uart1_receive_buf[2] =='D') && (uart1_receive_buf[3] =='N')) index=2;
            if((uart1_receive_buf[2] =='L') && (uart1_receive_buf[3] =='U')) index=3;
            if((uart1_receive_buf[2] =='R') && (uart1_receive_buf[3] =='U')) index=4;
            if((uart1_receive_buf[2] =='L') && (uart1_receive_buf[3] =='D')) index=5;
            if((uart1_receive_buf[2] =='R') && (uart1_receive_buf[3] =='D')) index=6;
            len = uart1_receive_buf.length();  //获取串口接收数据的长度
            pwm=0;        
            for(i = 0; i < len; i++) {              //如果数据没有接收完
                if(uart1_receive_buf[i] == '-') {         //判断是否为起始符“#”
                    i++;                                  //下一个字符
                    while((uart1_receive_buf[i] != '>') && (i<len)) {  //判断是否为#后面的数字检测完
                        pwm =  pwm*10 + uart1_receive_buf[i] - '0';  //记录P之前的数字
                        i++;
                    }                     
                    //检测完后赋值
                   pwm_value=pwm;
                   myservo.writeMicroseconds(pwm_value);
                   index = pwm = time1 = 0; 
                }
             }
           } 
          else if(uart1_receive_buf[0] == '<' && (uart1_receive_buf[1] == 'B') && (uart1_receive_buf[2] == 'U') 
              && (uart1_receive_buf[3] == 'P') && (uart1_receive_buf[4] == 'D') && (uart1_receive_buf[5] == '>')) 
          {
             Motor_Forward(1,100);
             Motor_Forward(2,100);
             myservo.writeMicroseconds(1500);
             Serial.println("Foward");
          }    
          else if(uart1_receive_buf[0] == '<' && (uart1_receive_buf[1] == 'B') && (uart1_receive_buf[2] == 'D') 
              && (uart1_receive_buf[3] == 'N') && (uart1_receive_buf[4] == 'D') && (uart1_receive_buf[5] == '>')) 
          {
             Motor_Back(1,100);
             Motor_Back(2,100);
             myservo.writeMicroseconds(1500);
             Serial.println("Back");
          } 

         else if(uart1_receive_buf[0] == '<' && (uart1_receive_buf[1] == 'B') && (uart1_receive_buf[2] == 'L') 
              && (uart1_receive_buf[3] == 'T') && (uart1_receive_buf[4] == 'D') && (uart1_receive_buf[5] == '>')) 
          {
             Motor_Forward(1,100);
             Motor_Forward(2,100); 
             myservo.writeMicroseconds(1100); 
             Serial.println("Left");
          } 
         else if(uart1_receive_buf[0] == '<' && (uart1_receive_buf[1] == 'B') && (uart1_receive_buf[2] == 'R') 
              && (uart1_receive_buf[3] == 'T') && (uart1_receive_buf[4] == 'D') && (uart1_receive_buf[5] == '>')) 
          {
             Motor_Forward(1,100);
             Motor_Forward(2,100); 
             myservo.writeMicroseconds(1900); 
             Serial.println("Right");
          } 
         else if(uart1_receive_buf[0] == '<' && (uart1_receive_buf[1] == 'B') && (uart1_receive_buf[4] == 'U') && (uart1_receive_buf[5] == '>')) 
          {
                Motor_Stop(1); 
                Motor_Stop(2); 
          } 
                
        uart1_receive_buf = "";
}



