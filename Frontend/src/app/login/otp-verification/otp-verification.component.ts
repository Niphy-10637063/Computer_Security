import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-otp-verification',
  templateUrl: './otp-verification.component.html',
  styleUrls: ['./otp-verification.component.scss'],
})
export class OtpVerificationComponent {
  otp_number: any = '';
  constructor(private router: Router) {}
  onSubmit(): void {
  }
  redirect(): void {
    this.router.navigateByUrl('sign-in');
  }
}
