import { Component, OnInit } from '@angular/core';
import { NgForm } from '@angular/forms';
import { DataService } from 'src/app/core/common-services/data.service';
import * as JsEncryptModule from 'jsencrypt';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/core/authentication/auth.service';
import { privateKey, publicKey } from '../../core/config';
@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss'],
})
export class ChatComponent implements OnInit {
  encryptMod: any;
  userList: any = [];
  selectedUser: any = '';
  publicKey: any = '';
  message: string = '';
  userName: string = '';
  isUIEncryption: boolean = true;
  constructor(
    private dataService: DataService,
    private router: Router,
    private authService: AuthService,
    private snackBar: MatSnackBar
  ) {
    this.encryptMod = new JsEncryptModule.JSEncrypt();
  }

  ngOnInit(): void {
    const userInfo = this.authService.getUserFromStorage();
    if (userInfo) {
      this.userName = userInfo.userName;
    }
    this.getUsers();
  }

  private getUsers(): void {
    this.dataService.getUsers().subscribe((res: any) => {
      if (res && res.status == 200) {
        if (res.body && res.body.data && res.body.success) {
          this.userList = res.body.data;
        }
      }
    });
  }
  reviewMessage: string = '';
  messageList: any = [];
  onTabChanged(event: any): void {
    this.messageList = [];
    if (event && event.index == 1) {
      if (this.isUIEncryption) {
        this.dataService.getMessages().subscribe((res: any) => {
          if (res && res.body && res.body.data) {
            this.encryptMod.setPrivateKey(privateKey);
            res.body.data.forEach((element: any) => {
              element.message = this.encryptMod.decrypt(element.message);
            });
            this.messageList = res.body.data;
          }
        });
      } else {
        this.dataService.getUserMessages().subscribe((res: any) => {
          if (res && res.body && res.body.data) {
            this.messageList = res.body.data;
          }
        });
      }
    }
    console.log(event);
  }
  sendMessage(messageForm: NgForm): void {
    if (!messageForm.valid) {
      return;
    }
    // if (!this.publicKey) {
    //   return;
    // }

    if (this.isUIEncryption) {
      this.encryptMod.setPublicKey(publicKey);
      const message: any = this.encryptMod.encrypt(this.message);
      const body: any = {
        message: message,
      };
      this.dataService.send(body).subscribe({
        next: (res) => {
          if (res && res.status == 201 && res.body.success) {
            this.openSnackBar('Message sent successfully', false);
            messageForm.reset();
          } else {
            this.openSnackBar('Something went wrong', true);
          }
        },
        error: (err) => {
          if (err && err.error && err.error.message) {
            this.openSnackBar(err.error.message, true);
          } else {
            this.openSnackBar('Something went wrong', true);
          }
        },
      });
    } else {
      const body: any = {
        receiverId: this.selectedUser,
        message: this.message,
      };
      this.dataService.sendMessage(body).subscribe({
        next: (res) => {
          if (res && res.status == 201 && res.body.success) {
            this.openSnackBar('Message sent successfully', false);
            messageForm.reset();
          } else {
            this.openSnackBar('Something went wrong', true);
          }
        },
        error: (err) => {
          if (err && err.error && err.error.message) {
            this.openSnackBar(err.error.message, true);
          } else {
            this.openSnackBar('Something went wrong', true);
          }
        },
      });
    }
  }

  onSelect(): void {
    // this.dataService.getPublicKey(this.selectedUser).subscribe((res: any) => {
    //   if (res && res.status == 200) {
    //     if (res.body && res.body.data && res.body.success) {
    //       this.publicKey = res.body.data.publicKey;
    //     }
    //   }
    // });
  }
  public openSnackBar(message: string, hasError: boolean): any {
    const config: any = new MatSnackBarConfig();
    config.panelClass = hasError ? ['error-red'] : ['success-green'];
    config.duration = 5000;
    config.verticalPosition = 'bottom';
    this.snackBar.open(message, undefined, config);
  }

  logout(): void {
    this.authService.destroySession();
    this.router.navigateByUrl('sign-in');
  }
}
