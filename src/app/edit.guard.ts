import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

export class EditGuard implements CanActivate {
  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    let password: string | null = null; // Initialize password as null

    if (password === 'tuition') {
      return true; // Allow access to the route
    }

        while ( password !== 'tuition') {
      password = prompt('Enter the password:');

      if (password === null) {
        return false;
      }

      if ( password !== 'tuition') {
        alert('Incorrect password. Please try again.');
      }
    }

    return true;
  }
}

