import { Component,OnInit } from '@angular/core';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/core/authentication/auth.service';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.scss'],
})
export class SignInComponent implements OnInit {
  public userName: string = '';
  public password: string = '';
  public submitted: boolean = false;
  constructor(
    private router: Router,
    private snackbar: MatSnackBar,
    private authService: AuthService
  ) {}
  ngOnInit(): void {
   if(this.authService.isLoggedIn()){
    this.router.navigateByUrl('chat');
   }
  }

  onSubmit(): void {
    const body: any = {
      username: this.userName,
      password: this.password,
    };
    this.authService.login(body).subscribe({
      next: (res: any) => {
        if (res && res.body && res.body.success) {
          this.submitted = false;
          this.authService.setSession(res.body);
          this.router.navigateByUrl('chat');
        } else {
          this.submitted = false;
        }
      },
      error: (error: any) => {
        console.log(error);
        if (error && error.error && error.error.success == false)
          this.submitted = false;
        this.openSnackBar(error.error.message, true);
      },
    });
  }
  redirect(): void {
    this.router.navigateByUrl('sign-up');
  }
  forgot(): void {
    this.router.navigateByUrl('forgot-password');
  }
  public openSnackBar(message: string, hasError: boolean): any {
    const config: any = new MatSnackBarConfig();
    config.panelClass = hasError ? ['error-red'] : ['success-green'];
    config.duration = 5000;
    config.verticalPosition = 'top';
    this.snackbar.open(message, undefined, config);
  }
}
