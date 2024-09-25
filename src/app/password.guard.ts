import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

export class PasswordGuard implements CanActivate {
  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    let password: string | null = null; // Initialize password as null

    if (password === 'maity@29') {
      return true; // Allow access to the route
    }

        while (password !== 'maity@29' && password !== 'tuition') {
      password = prompt('Enter the password:');

      if (password === null) {
        return false;
      }

      if (password !== 'maity@29' && password !== 'tuition') {
        alert('Incorrect password. Please try again.');
      }
    }

    return true;
  }
}
