import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RecoverPasswoordComponent } from './recover-passwoord.component';

describe('RecoverPasswoordComponent', () => {
  let component: RecoverPasswoordComponent;
  let fixture: ComponentFixture<RecoverPasswoordComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RecoverPasswoordComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RecoverPasswoordComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
