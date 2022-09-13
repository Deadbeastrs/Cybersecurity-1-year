void main(void)

{
  char 0;
  undefined uVar1;
  int len_temp_hist;
  int iVar2;
  int iVar3;
  uint uVar4;
  int i;
  uint temp;
  uint LEDS_LAT_1;
  uint temp2;
  undefined temp_hist [64];
  char real_temp;
  char real_temp_2;
  char temp_offset;
  char temp_offset_2 [5];
  int local_88;
  uint local_84 [11];
  int local_58;
  uint local_54 [11];
  undefined *temp_hist1;
  
  temp_offset = '\0';
  temp_offset_2[0] = '\0';
  FUN_9d003118(0x23);
  FUN_9d003158(0x1f);
  local_88 = 0;
  local_58 = 0;
  FUN_9d001898(0x4b00,8,0x4f,2);
  FUN_9d00157c();
  FUN_9d00154c(200000);
  FUN_9d001400(90000);
  FUN_9d0019e8();
  FUN_9d001a60(1);
  FUN_9d0021d4();
  FUN_9d001af8();
  if (-1 < _DAT_bf8860d0 << 0x17) {
    first_setup();
  }
  printRS232("Reverse Engineering\n");
  Status = Status | 1;
  setpoint_right = read_memory(0x43);
  setpoint_left = read_memory(0x44);
  setpoint_avg = read_memory(0x45);
  do {
    do {
    } while (iGpffff803c == 0);
    iGpffff803c = 0;
    if (uGpffff8048 != (_PORT_SWITCH << 0x1c) >> 0x1e) {
      cGpffff8029 = '\x01';
    }
    uGpffff8048 = (_PORT_SWITCH << 0x1c) >> 0x1e;
                    // SETUP OR NORMAL MODE
    if (uGpffff8048 == 0) {
                    // SETUP MODE
      OCs(0,0);
      if (uGpffff8044 != (_PORT_SWITCH & 3)) {
        cGpffff8029 = '\x01';
      }
      uGpffff8044 = _PORT_SWITCH & 3;
                    // Board OFF (2leds light up)
      if (uGpffff8044 == 0) {
        _LEDS_LAT = _LEDS_LAT & 0xff00 | 0x24;
      }
      else {
        len_temp_hist = get_potenciometer();
        LEDS_LAT_1 = (len_temp_hist * 0x40 + 0x1ff) / 0x3ff + 0x23;
                    // Value for set point
        uGpffff8040 = display(LEDS_LAT_1 & 0xff);
                    // DIP 1,2 our both
        if (uGpffff8044 == 1) {
          _LEDS_LAT = _LEDS_LAT & 0xff00 | 1;
          uGpffff8018 = LEDS_LAT_1;
        }
        if (uGpffff8044 == 2) {
          _LEDS_LAT = _LEDS_LAT & 0xff00 | 0x80;
          uGpffff8014 = LEDS_LAT_1;
        }
        if (uGpffff8044 == 3) {
          _LEDS_LAT = _LEDS_LAT & 0xff00 | 0x81;
          uGpffff8010 = LEDS_LAT_1;
        }
      }
    }
    else {
                    // NORMAL MODE
      if ((iGpffff8034 != 0) || (cGpffff8029 == '\x01')) {
        cGpffff8029 = '\0';
        iGpffff8034 = 0;
        real_temp = get_real_temp();
        len_temp_hist = get_real_temp(1);
        real_temp_2 = (char)len_temp_hist;
        if (real_temp == -1) {
          printRS232("I2C Error (A0)");
        }
        else if (len_temp_hist == -1) {
          printRS232("I2C Error (A4)\n");
        }
        else {
          temp_offset_logic('\0',&real_temp,&temp_offset,&real_temp_2,temp_offset_2);
          len_temp_hist = local_88;
          temp = (int)real_temp + (int)temp_offset;
          temp2 = (int)real_temp_2 + (int)temp_offset_2[0];
          local_88 = local_88 + 1;
          local_84[len_temp_hist] = temp;
          local_54[local_58] = temp2;
          local_58 = local_58 + 1;
                    // MODE IF for OCs and LEDs
                    // 
          LEDS_LAT_1 = (uint)(char)((int)(temp + temp2) / 2);
          if (uGpffff8048 == 1) {
            uGpffff8040 = display(temp & 0xff);
            OCs((int)((setpoint_right - temp) * 0x2d) / 10,0);
            temp2 = _LEDS_LAT & 0xfff0;
            LEDS_LAT_1 = led_formula(0x23,setpoint_right,temp,4,0);
            _LEDS_LAT = (temp2 | LEDS_LAT_1) & 0xff0f;
          }
          else if (uGpffff8048 == 2) {
            uGpffff8040 = display(temp2 & 0xff);
            OCs(0,(int)((setpoint_left - temp2) * 0x2d) / 10);
            LEDS_LAT_1 = _LEDS_LAT & 0xff00;
            _LEDS_LAT = _LEDS_LAT & 0xfff0;
            len_temp_hist = led_formula(0x23,setpoint_left,temp2,4,1);
            _LEDS_LAT = LEDS_LAT_1 | len_temp_hist << 4;
          }
          else if (uGpffff8048 == 3) {
            uGpffff8040 = display(LEDS_LAT_1 & 0xff);
            OCs((int)((setpoint_avg - LEDS_LAT_1) * 0x2d) / 10,
                (int)((setpoint_avg - LEDS_LAT_1) * 0x2d) / 10);
            uVar4 = _LEDS_LAT & 0xfff0;
            LEDS_LAT_1 = led_formula(0x23,setpoint_avg,temp,4,0);
            uVar4 = uVar4 | LEDS_LAT_1;
            _LEDS_LAT = uVar4;
            len_temp_hist = led_formula(0x23,setpoint_avg,temp2,4,1);
            _LEDS_LAT = uVar4 & 0xff0f | len_temp_hist << 4;
          }
          len_temp_hist = local_58;
          i = 0;
          if (local_88 == (local_88 / 5) * 5) {
            iVar2 = 0;
            temp_hist1 = temp_hist;
            iVar3 = local_88;
            if (0 < local_88) {
              do {
                iVar3 = iVar3 + -1;
                iVar2 = iVar2 + *(int *)(temp_hist1 + 0x4c);
                i = i + *(int *)(temp_hist1 + 0x7c);
                temp_hist1 = temp_hist1 + 4;
              } while (iVar3 != 0);
            }
            iVar2 = iVar2 / local_88;
            if (local_88 == 0) {
              trap(7);
            }
            local_88 = 0;
            local_58 = 0;
            if (len_temp_hist == 0) {
              trap(7);
            }
            Write_temp_history((char)iVar2,(char)(i / len_temp_hist));
          }
        }
      }
      0 = FUN_9d0030f8();
      temp_offset_logic(0,&real_temp,&temp_offset,&real_temp_2,temp_offset_2);
    }
                    // RS232C
                    // 
    if (iGpffff802c == 1) {
      iGpffff802c = 0;
      i = 0;
      len_temp_hist = Read_temperature_history(temp_hist);
      printRS232("\nTemperatures:\n");
      temp_hist1 = temp_hist;
      if (0 < len_temp_hist) {
        do {
          i = i + 2;
          print_rs232_numTOascii(*temp_hist1);
                    // print_space
                    // 
          print_rs232_1(0x20);
          temp_hist1 = temp_hist1 + 2;
        } while (i < len_temp_hist);
      }
      i = 0;
      printRS232("\n");
      temp_hist1 = temp_hist;
      if (0 < len_temp_hist) {
        do {
          i = i + 2;
          print_rs232_numTOascii(temp_hist1[1]);
          print_rs232_1(0x20);
          temp_hist1 = temp_hist1 + 2;
        } while (i < len_temp_hist);
      }
      len_temp_hist = 0;
      printRS232("\nSet Points:\n");
      do {
        uVar1 = read_memory(len_temp_hist + 0x43);
        print_rs232_numTOascii(uVar1);
        len_temp_hist = len_temp_hist + 1;
        print_rs232_1(0x20);
      } while (len_temp_hist < 3);
    }
  } while( true );
}


undefined4 read_memory(void)

{
  uint uVar1;
  
  do {
    uVar1 = FUN_9d00165c();
  } while ((uVar1 & 1) != 0);
  do {
  } while (_DAT_bf805a10 << 0x14 < 0);
  _DAT_bf805a20 = 0;
  return 0;
}

void Write_mem(undefined4 param_1,uint param_2)

{
  uint uVar1;
  
  do {
    uVar1 = FUN_9d00165c();
  } while ((uVar1 & 1) != 0);
  do {
  } while (_DAT_bf805a10 << 0x14 < 0);
  do {
  } while (_DAT_bf805a10 << 0x14 < 0);
  _DAT_bf805a20 = param_2 & 0xff;
  return;
}

void print_rs232_1(char param_1)

{
  do {
  } while (_DAT_bf806010 << 0x16 < 0);
  _DAT_bf806020 = (int)param_1;
  return;
}

void printRS232(char *param_1)

{
  for (; *param_1 != '\0'; param_1 = param_1 + 1) {
    print_rs232_1();
  }
  return;
}

void first_setup(void)

{
  Write_mem(0x41,0);
  Write_mem(0x42,0);
  Write_mem(0x43,0x32);
  Write_mem(0x44,0x32);
  Write_mem(0x45,0x32);
  return;
}



// WARNING: Globals starting with '_' overlap smaller symbols at the same address

void OCs(int percent_side_1,int percent_side_2)

{
  if (100 < percent_side_1) {
    percent_side_1 = 100;
  }
  if (percent_side_1 < 0) {
    percent_side_1 = 0;
  }
  if (100 < percent_side_2) {
    percent_side_2 = 100;
  }
  if (percent_side_2 < 0) {
    percent_side_2 = 0;
  }
  _DAT_bf803020 = (uint)(_DAT_bf800820 * percent_side_1 + percent_side_1) / 100;
  _DAT_bf803220 = (uint)(_DAT_bf800820 * percent_side_2 + percent_side_2) / 100;
  return;
}


undefined4 get_potenciometer(void)

{
  do {
  } while (-1 < (int)(_DAT_bf881040 << 0x1e));
  _DAT_bf881040 = _DAT_bf881040 & 0xfffffffd;
  DAT_bf809000 = DAT_bf809000 | 4;
  return _DAT_bf809070;
}



uint display(uint param_1)

{
  return (param_1 & 0xff) + ((param_1 & 0xff) / 10) * 6 & 0xff;
}



undefined4 get_real_temp(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  
  uVar4 = 0xffffffff;
  uVar2 = 0x90;
  uVar3 = 0x91;
  if (param_1 != 0) {
    uVar2 = 0x98;
    uVar3 = 0x99;
  }
  FUN_9d001444();
  iVar1 = FUN_9d0014b0(uVar2);
  if ((iVar1 == 0) && (iVar1 = FUN_9d0014b0(0), iVar1 == 0)) {
    FUN_9d001444();
    iVar1 = FUN_9d0014b0(uVar3);
    if (iVar1 == 0) {
      uVar4 = FUN_9d0014e0(1);
    }
  }
  FUN_9d001470();
  return uVar4;
}



void temp_offset_logic(char 0,char *param_2,char *param_3,char *param_4,char *param_5)

{
  char cVar1;
  int iVar2;
  char cVar3;
  
  if (0 == '1') {
    cVar1 = *param_3 + '\x01';
LAB_9d001d4c:
    *param_3 = cVar1;
  }
  else {
    if (0 == 'q' || 0 == 'Q') {
      cVar1 = *param_3 + -1;
      goto LAB_9d001d4c;
    }
    if (0 == 'a' || 0 == 'A') {
      *param_3 = '\0';
    }
    else if (0 == '2') {
      *param_5 = *param_5 + '\x01';
    }
    else if (0 == 'w' || 0 == 'W') {
      *param_5 = *param_5 + -1;
    }
    else {
      if (0 != 's' && 0 != 'S') {
        cVar1 = *param_2;
        goto LAB_9d001d54;
      }
      *param_5 = '\0';
    }
  }
  cVar1 = *param_2;
LAB_9d001d54:
  if ((int)cVar1 + (int)*param_3 < 100) {
    iVar2 = (int)cVar1 + (int)*param_3;
  }
  else {
    cVar3 = 'c' - cVar1;
    *param_3 = cVar3;
    cVar1 = *param_2;
    iVar2 = (int)cVar1 + (int)cVar3;
  }
  if (iVar2 < 0) {
    *param_3 = '#' - cVar1;
  }
  cVar1 = *param_4;
  if ((int)cVar1 + (int)*param_5 < 100) {
    iVar2 = (int)cVar1 + (int)*param_5;
  }
  else {
    cVar3 = 'c' - cVar1;
    *param_5 = cVar3;
    cVar1 = *param_4;
    iVar2 = (int)cVar1 + (int)cVar3;
  }
  if (-1 < iVar2) {
    return;
  }
  *param_5 = '#' - cVar1;
  return;
}



int led_formula(int 0x23,int set_point,int temp,uint 4,int chamber_0_1_)

{
  int var1;
  int 16;
  uint uVar1;
  
  if (temp < 0x23) {
    temp = 0x23;
  }
                    // 15
  var1 = (1 << (4 & 0x1f)) + -1;
  if (temp <= set_point) {
    var1 = (int)((set_point - 0x23) * 2 + 4) / (int)(4 << 1);
    if (4 << 1 == 0) {
      trap(7);
    }
    16 = 1 << (4 & 0x1f);
    if (var1 == 0) {
      var1 = 1;
    }
    if (var1 == 0) {
      trap(7);
    }
    uVar1 = (temp - 0x23) / var1 + 1;
    if ((int)uVar1 <= (int)4) {
      4 = uVar1;
    }
    var1 = (1 << (4 & 0x1f)) + -1;
    if (chamber_0_1_ != 1) {
      var1 = 16 - (16 >> (4 & 0x1f));
    }
  }
  return var1;
}



void Write_temp_history(char param_1,char param_2)

{
  int iVar1;
  int iVar2;
  
  iVar1 = read_memory(0x42);
  iVar2 = read_memory(0x41);
  Write_mem(iVar2 + 5,(int)param_1);
  Write_mem(iVar2 + 6,(int)param_2);
  if (0x3b < iVar1) {
    Write_mem(0x41,(iVar2 + 2) % 0x3c);
    return;
  }
  Write_mem(0x42,iVar1 + 2);
  Write_mem(0x41,(iVar2 + 2) % 0x3c);
  return;
}



int Read_temperature_history(int param_1)

{
  undefined uVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  undefined *puVar5;
  
  iVar2 = read_memory(0x42);
  iVar3 = read_memory(0x41);
  if (iVar2 < 0x3c) {
    iVar3 = 0;
    if (0 < iVar2) {
      do {
        uVar1 = read_memory(iVar3 + 5);
        puVar5 = (undefined *)(param_1 + iVar3);
        iVar4 = iVar3 + 6;
        *puVar5 = uVar1;
        iVar3 = iVar3 + 2;
        uVar1 = read_memory(iVar4);
        puVar5[1] = uVar1;
      } while (iVar3 < iVar2);
    }
    return iVar2;
  }
  iVar4 = 0;
  do {
    uVar1 = read_memory(iVar3 + 5);
    puVar5 = (undefined *)(param_1 + iVar4);
    *puVar5 = uVar1;
    uVar1 = read_memory(iVar3 + 6);
    iVar4 = iVar4 + 2;
    puVar5[1] = uVar1;
    iVar3 = (iVar3 + 2) % 0x3c;
  } while (iVar4 < 0x3c);
  return iVar2;
}



void print_rs232_numTOascii(undefined param_1)

{
  uint uVar1;
  
  uVar1 = display(param_1);
  print_rs232_1((int)(char)((char)(uVar1 >> 4) + '0'));
  print_rs232_1((uVar1 & 0xf) + 0x30);
  return;
}


void Display_number(uint param_1,char param_2)

{
  _DAT_bf8860e0 = _DAT_bf8860e0 ^ 0x60;
  if (param_2 != 0) {
    _DAT_bf886060 = _DAT_bf886060 & 0x80ff | 0x100 << (param_2 * 3 - 3U & 0x1f);
    return;
  }
  if ((_DAT_bf8860e0 & 0x20) != 0) {
    _DAT_bf886060 =
         _DAT_bf886060 & 0x80ff | (int)*(char *)((int)&DAT_a0000000 + (param_1 & 0xf)) << 8;
    return;
  }
  _DAT_bf886060 =
       _DAT_bf886060 & 0x80ff | (int)*(char *)((int)&DAT_a0000000 + ((param_1 & 0xff) >> 4)) << 8;
  return;
}
