import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';
import { AuthenticationGuard } from './core/authentication/authentication.guard';

const routes: Routes = [
  {
    path: 'chat',
    loadChildren: () =>
      import('./chat/chat.module').then((m) => m.ChatModule),
    canActivate:[AuthenticationGuard]
  },
  {
    path: '',
    loadChildren: () =>
      import('./login/login.module').then((m) => m.LoginModule),
  },
  {
    path: 'unauthorized-access-401',
    loadChildren: () =>
      import('./unauthorised/unauthorised.module').then(
        (m) => m.UnauthorisedModule
      ),
  },
  {
    path: '**',
    loadChildren: () =>
      import('./page-not-found/page-not-found.module').then(
        (m) => m.PageNotFoundModule
      ),
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes,{preloadingStrategy: PreloadAllModules, initialNavigation:'enabledBlocking' })],
  exports: [RouterModule],
})
export class AppRoutingModule {}
