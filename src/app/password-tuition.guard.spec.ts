import { TestBed } from '@angular/core/testing';
import { CanActivateFn } from '@angular/router';

import { passwordTuitionGuard } from './password-tuition.guard';

describe('passwordTuitionGuard', () => {
  const executeGuard: CanActivateFn = (...guardParameters) => 
      TestBed.runInInjectionContext(() => passwordTuitionGuard(...guardParameters));

  beforeEach(() => {
    TestBed.configureTestingModule({});
  });

  it('should be created', () => {
    expect(executeGuard).toBeTruthy();
  });
});
